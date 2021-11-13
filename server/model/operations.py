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
        query = "select room_id from rooms where 0 = (select count(*) from room_unavailability where room_unavailability.room_id = rooms.room_id and room_unavail_date = %s and (room_start_time between %s and %s or room_end_time between %s and %s))"
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

    def getAvailTimeSlots(self, arr, duration):
        def convert_time(time_str):
            date_var = time.strptime(time_str, '%H:%M:%S')
            return date_var

        t_duration = time.strptime(duration, '%H:%M:%S')
        dh = t_duration.tm_hour
        dm = t_duration.tm_min
        ds = t_duration.tm_sec

        avail_times = []

        for idx in range(0, len(arr)):
            if idx == len(arr) - 1: # last case
                t2 = convert_time(str(arr[idx][1])) # get end_time
                t2h = t2.tm_hour; t2m = t2.tm_min; t2s = t2.tm_sec
                dsc = ds; dmc = dm; dhc = dh

                ns = t2s + dsc
                if ns >= 60:
                    ns -= 60
                    dmc += 1
                
                nm = t2m + dmc
                if nm >= 60:
                    nm -= 60
                    dhc += 1
                
                nh = t2h + dhc
                if nh >= 24:
                    print("time goes beyond specifed date")
                    continue

                avail_ts = str(t2h) + ":" + str(t2m) + ":" + str(t2s) + "-" + str(nh) + ":" + str(nm) + ":" + str(ns)
                avail_times.append(avail_ts)


            elif idx > 0: # 1 to len(n) - 2
                t2 = convert_time(str(arr[idx][1])) # get end_time
                t2h = t2.tm_hour; t2m = t2.tm_min; t2s = t2.tm_sec
                dsc = ds; dmc = dm; dhc = dh

                ns = t2s + dsc
                if ns >= 60:
                    ns -= 60
                    dmc += 1
                
                nm = t2m + dmc
                if nm >= 60:
                    nm -= 60
                    dhc += 1
                
                nh = t2h + dhc

                t3 = convert_time(str(arr[idx+1][0])) # get next start_time
                t3h = t3.tm_hour; t3m = t3.tm_min; t3s = t3.tm_sec
                avail_ts = str(t2h) + ":" + str(t2m) + ":" + str(t2s) + "-" + str(nh) + ":" + str(nm) + ":" + str(ns)

                if nh < t3h:
                    avail_times.append(avail_ts)
                elif nh == t3h:
                    if nm < t3m:
                        avail_times.append(avail_ts)
                    elif nm == t3m:
                        if ns < t3s:
                            avail_times.append(avail_ts)

            else: # first case
                t = convert_time(str(arr[idx][0])) # get start_time
                t1h = t.tm_hour; t1m = t.tm_min; t1s = t.tm_sec
                
                ns = t1s - ds if t1s >= ds else 60 + t1s - ds
                if t1s < ds:
                    t1m -= 1

                nm = t1m - dm if t1m >= dm else 60 + t1m - dm
                if t1m < dm:
                    t1h -= 1
                
                nh = t1h - dh
                if nh < 0:
                    print("time goes before specified date")
                    continue
                
                avail_ts = str(nh) + ":" + str(nm) + ":" + str(ns) + "-" + str(t1h) + ":" + str(t1m) + ":" + str(t1s)
                avail_times.append(avail_ts)

        if len(avail_times) == 0:
            print("No available time slots")
        else:
            return avail_times

    # def findAvailableTimeSlot(self, schedule_start_time, schedule_end_time):
    def findAvailableTimeSlot(self, date, duration, invitees):
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
        
        return self.getAvailTimeSlots(self.removeBetweens(interval_tuples), duration)
        

    #########12. User Statistic########

    #a. Most used Room
    def getMostUsedRoom(self, user_id):
        cursor = self.conn.cursor()
        query = "select room_id from schedule as s inner join invitee as i on s.schedule_id = i.schedule_id where i.user_id=%s group by room_id order by count (i.user_id) desc limit 1"
        cursor.execute(query,(user_id,))
        result = cursor.fetchone()
        if not result:
            return 'error'
        return result[0]

    #b. User logged in user has been most booked with
    def getMostBookedWithUser(self, user_id):
        cursor = self.conn.cursor()
        query = "select i2.user_id from invitee as i1 inner join invitee as i2 on i1.schedule_id = i2.schedule_id where i1.user_id = %s and i1.user_id <> i2.user_id group by i2.user_id order by count(*) desc limit 1"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if not result:
            return 'error'
        return result[0]

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
        query = "select user_id, count(user_id) from invitee group by user_id order by count(user_id) desc limit 10"
        cursor.execute(query,)
        result = []
        for row in cursor:
            result.append(row)
        return result

    #c. Find most booked rooms (Find top 10)
    def getMostBookedRooms(self):
        cursor = self.conn.cursor()
        query = "select room_id, count(room_id) from schedule group by room_id order by count(room_id) desc limit 10"
        cursor.execute(query,)
        result = []
        for row in cursor:
            result.append(row)
        return result