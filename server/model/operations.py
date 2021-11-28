from config.dbconfig import pg_config
import psycopg2
import time

class OperationsDAO():
    def __init__(self) -> None:
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" %(pg_config['dbname'], pg_config['user'], pg_config['password'],
                                                                            pg_config['port'], pg_config['host'])
        self.conn = psycopg2.connect(connection_url)
    
    #2. Find an available room (lab, classroom, study space, etc.) at a time frame
    def getAllAvailableRooms(self, room_unavail_date, room_start_time, room_end_time):
        cursor = self.conn.cursor()
        query = "select room_id, room_name from rooms where 0 = (select count(*) from room_unavailability where room_unavailability.room_id = rooms.room_id and room_unavail_date = %s and (room_start_time between %s and %s or room_end_time between %s and %s))"
        cursor.execute(query, (room_unavail_date, room_start_time, room_end_time, room_start_time, room_end_time),)
        result = []
        for row in cursor:
            result.append(row)
        return result

    #3. Find who appointed a room at a certain time
    def whoAppointedRoom(self, room_id, user_id, date, time):
        cursor = self.conn.cursor()
        query = "select user_id from schedule as s where room_id = %s and schedule_date = %s and %s between schedule_start_time and schedule_end_time and (select authorization_level from users as u where u.user_id = %s) >= (select authorization_level from rooms as r where r.room_id = %s)"
        cursor.execute(query, (room_id, date, time, user_id, room_id,))
        uid = cursor.fetchone()
        if not uid:
            return 'error'
        else:
            uid = uid[0]
        return uid

    #4. Give an all-day schedule for a room
    def getRoomAllDaySchedule(self, room_id, user_id, room_unavail_date):
        cursor = self.conn.cursor()
        query = "select room_start_time, room_end_time from room_unavailability where room_id=%s and room_unavail_date=%s and (select authorization_level from users as u where u.user_id = %s) >= (select authorization_level from rooms as r where r.room_id = %s) group by room_unavail_date, room_start_time, room_end_time order by room_start_time, room_end_time"
        cursor.execute(query, (room_id, room_unavail_date, user_id, room_id))
        result = []
        for row in cursor:
            result.append(row)
        return result

    #5. Give an all-day schedule for a user
    def getAllDayScheduleforUser(self, user_id, user_date):
        cursor = self.conn.cursor()
        query = "select user_start_time, user_end_time from user_unavailability where user_id=%s and user_date=%s group by user_date, user_start_time, user_end_time order by user_start_time, user_end_time"
        cursor.execute(query, (user_id, user_date,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    #8. Find a time that is free for everyone in the meeting

    ### Helper functions ###
    def removeBetweens(self, arr: list[tuple]):
        found = False
        for c in arr:
            t_c1 = time.strptime(str(c[0]), '%H:%M:%S') # curr start_time
            t_c2 = time.strptime(str(c[1]), '%H:%M:%S') # curr end_time
            for cmp in arr:
                if c == cmp:
                    continue
                t_cmp1 = time.strptime(str(cmp[0]), '%H:%M:%S') # cmp start_time
                t_cmp2 = time.strptime(str(cmp[1]), '%H:%M:%S') # cmp end_time
                if (t_c1 >= t_cmp1) and (t_c2 <= t_cmp2):
                    arr.remove(c)
                    found = True
                    break
            if found:
                break
        if found:
            return self.removeBetweens(arr)
        else:
            return arr

    def getAvailTimeSlots(self, arr):
        def convert_time(time_str):
            date_var = time.strptime(time_str, '%H:%M:%S')
            return date_var

        def create_interval(start: time.struct_time, end: time.struct_time):
            sh = str(start.tm_hour)
            sh = sh if sh != '0' else '00'
            sm = str(start.tm_min)
            sm = sm if sm != '0' else '00'
            ss = str(start.tm_sec)
            ss = ss if ss != '0' else '00'
            s = sh + ':' + sm + ':' + ss
            eh = str(end.tm_hour)
            eh = eh if eh != '0' else '00'
            em = str(end.tm_min)
            em = em if em != '0' else '00'
            es = str(end.tm_sec)
            es = es if es != '0' else '00'
            e = eh + ':' + em + ':' + es
            
            return s + '-' + e

        def firstStartTime(arr):
            first = convert_time(str(arr[0][0]))
            for i in range(1, len(arr)):
                curr = convert_time(str(arr[i][0]))
                if curr < first:
                    first = curr
            return first

        def lastEndTime(arr):
            last = convert_time(str(arr[0][1]))
            for i in range(1, len(arr)):
                curr = convert_time(str(arr[i][1]))
                if curr > last:
                    last = curr
            return last

        avail_times = []

        for idx in range(0, len(arr)):
            if idx == 0: # first case
                first_time = firstStartTime(arr)
                b = time.strptime('00:00:00', '%H:%M:%S')
                if b < first_time:
                    avail_times.append(create_interval(b, first_time))

            if idx == len(arr) - 1: # last case
                last_time = lastEndTime(arr)
                ending = time.strptime('23:59:59', '%H:%M:%S')
                if last_time < ending:
                    avail_times.append(create_interval(last_time, ending))

            # all cases
            if idx < len(arr) - 1: # can check with next one
                curr_e = convert_time(str(arr[idx][1]))
                next_s = convert_time(str(arr[idx+1][0]))
                if next_s > curr_e:
                    avail_times.append(create_interval(curr_e, next_s))

        return avail_times

    # def findAvailableTimeSlot(self, schedule_start_time, schedule_end_time):
    def findAvailableTimeSlot(self, date, invitees):
        cursor = self.conn.cursor()

        # Verify if there are invitees
        if len(invitees) == 0:
            return 'missing_invitees'
        
        query = "select user_start_time, user_end_time from user_unavailability where user_date = %s and ("
        for idx in range(0, len(invitees)):
            if idx > 0:
                query += " or user_id = {}".format(invitees[idx])
            else:
                query += "user_id = {}".format(invitees[idx])
        query += ") group by user_start_time, user_end_time"

        cursor.execute(query, (date,))

        interval_tuples = []
        for row in cursor:
            interval_tuples.append(row)
        
        if len(interval_tuples) == 0:
            return 'all_free'
        
        return self.getAvailTimeSlots(self.removeBetweens(interval_tuples))
        

    #########12. User Statistic########

    #a. Most used Room
    def getMostUsedRoom(self, user_id):
        cursor = self.conn.cursor()
        query = "select room_id, count(i.user_id), room_name from schedule as s inner join invitee as i on s.schedule_id = i.schedule_id natural inner join rooms where i.user_id=%s group by room_id, room_name order by count (i.user_id) desc limit 1"
        cursor.execute(query,(user_id,))
        result = cursor.fetchone()
        if not result:
            return 'error'
        return result

    #b. User logged in user has been most booked with
    def getMostBookedWithUser(self, user_id):
        cursor = self.conn.cursor()
        query = "select i2.user_id, count(*), u.first_name, u.last_name from invitee as i1 inner join invitee as i2 on i1.schedule_id = i2.schedule_id inner join users as u on u.user_id = i2.user_id where i1.user_id = %s and i1.user_id <> i2.user_id group by i2.user_id, u.first_name, u.last_name order by count(*) desc limit 1"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if not result:
            return 'error'
        return result

    #########13. Global Statistic########
    
    #a. Find busiest hours (Find top 5)
    def getBusiestHours(self):
        cursor = self.conn.cursor()
        query = "select schedule_start_time, schedule_end_time, count(*) from schedule group by schedule_start_time, schedule_end_time order by count(*) desc limit 5"
        cursor.execute(query,)
        result = []
        for row in cursor:
            result.append(row)
        return result

    #b. Find most booked users (Find top 10)
    def getMostBookedUsers(self):
        cursor = self.conn.cursor()
        query = "select user_id, count(user_id), first_name, last_name from invitee natural inner join users group by user_id, first_name, last_name order by count(user_id) desc limit 10"
        cursor.execute(query,)
        result = []
        for row in cursor:
            result.append(row)
        return result

    #c. Find most booked rooms (Find top 10)
    def getMostBookedRooms(self):
        cursor = self.conn.cursor()
        query = "select room_id, count(room_id), room_name from schedule natural inner join rooms group by room_id, room_name order by count(room_id) desc limit 10"
        cursor.execute(query,)
        result = []
        for row in cursor:
            result.append(row)
        return result