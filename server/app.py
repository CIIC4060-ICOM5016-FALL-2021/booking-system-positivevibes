from flask import Flask, request, make_response
from flask.json import jsonify
from controllers.users import Users
from controllers.building import Building
from controllers.schedule import Schedule
from controllers.rooms import Rooms
from controllers.invitee import Invitee
from controllers.room_unavailability import RoomUnavailability
from controllers.user_unavailability import UserUnavailability
from controllers.operations import Operations

app = Flask(__name__)


@app.route('/API')
def hello_world():  # put application's code here
    return 'PosVibesDB!'

@app.route('/API/users', methods=['GET', 'POST', 'PUT'])
def user_route():
    if request.method == 'GET':
        res = make_response (Users().getAllUsers())
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'POST':
        return Users().insertUser(request.json)
    elif request.method == 'PUT':
        return Users().updateUser(request.json)
    else:
        return {
            "error": "No such route"
        }

@app.route('/API/users/<int:user_id>', methods=['GET', 'DELETE'])
def user_byid_route(user_id):
    if request.method == 'GET':
        return Users().getUserById(user_id)
    elif request.method == 'DELETE':
        return Users().deleteUser(user_id)
    else:
        return {
            "error": "No such route"
        }

#Give an all-day schedule for a user
@app.route('/API/users/schedule', methods=['GET'])
def user_schedule():
    if request.method == 'GET':
        return Operations().getAllDayScheduleforUser(request.json)
    else:
        return {
            "error": "No such route"
        }

#12.a Most used Room
@app.route('/API/users/statistics/<int:user_id>/room', methods=['GET'])
def user_stat_room(user_id):
    if request.method == 'GET':
        return Operations().getMostUsedRoom(user_id)
    else:
        return {
            "error": "No such route"
        }

#12b. User logged in user has been most booked with
@app.route('/API/users/statistics/<int:user_id>/user', methods=['GET'])
def user_stat_user(user_id):
    if request.method == 'GET':
        return Operations().getMostBookedWithUser(user_id)
    else:
        return {
            "error": "No such route"
        }

@app.route('/API/schedule', methods=['GET', 'POST', 'PUT'])
def schedule_route():
    if request.method == 'GET':
        return Schedule().getAllSchedules()
    elif request.method == 'POST':
        return Schedule().insertSchedule(request.json)
    elif request.method == 'PUT':
        return Schedule().updateSchedule(request.json)
    else:
        return {
            "error": "No such route"
        }

@app.route('/API/schedule/<int:schedule_id>', methods=['GET', 'DELETE'])
def schedule_byid_route(schedule_id):
    if request.method == 'GET':
        return Schedule().getScheduleById(schedule_id)
    elif request.method == 'DELETE':
        return Schedule().deleteSchedule(schedule_id)
    else:
        return {
            "error": "No such route"
        }

#8. Find a time that is free for everyone in the meeting
@app.route('/API/schedule/available', methods=['GET'])
def schedule_find_timeslots():
    if request.method == 'GET':
        return Operations().findAvailableTimeSlot(request.json)
    else:
        return {
            "error": "No such route"
        }

@app.route('/API/user_unavailability', methods=['GET', 'POST', 'PUT'])
def user_unavail_route():
    if request.method == 'GET':
        return UserUnavailability().getAllUnavailableUsers()
    elif request.method == 'POST':
        return UserUnavailability().insertUnavailableUser(request.json)
    elif request.method == 'PUT':
        return UserUnavailability().updateUnavailableUser(request.json)
    else:
        return {
            "error": "No such route"
        }

@app.route('/API/user_unavailability/<int:user_unavail_id>', methods=['GET', 'DELETE'])
def user_unavail_byid_route(user_unavail_id):
    if request.method == 'GET':
        return UserUnavailability().getUnavailableUserById(user_unavail_id)
    elif request.method == 'DELETE':
        return UserUnavailability().deleteUnavailableUser(user_unavail_id)
    else:
        return {
            "error": "No such route"
        }

@app.route('/API/rooms', methods=['GET', 'POST', 'PUT'])
def rooms_route():
    if request.method == 'GET':
        return Rooms().getAllRooms()
    elif request.method == 'POST':
        return Rooms().insertRoom(request.json)
    elif request.method == 'PUT':
        return Rooms().updateRoom(request.json)
    else:
        return {
            "error": "No such route"
        }

@app.route('/API/rooms/<int:room_id>/<int:user_id>', methods=['GET'])
def rooms_auth_route(room_id, user_id):
    if request.method == 'GET':
        return Rooms().getRoomWithAuth(room_id, user_id)
    else:
        return {
            "error": "No such route"
        }

@app.route('/API/rooms/<int:room_id>', methods=['GET', 'DELETE'])
def rooms_byid_route(room_id):
    if request.method == 'GET':
        return Rooms().getRoomById(room_id)
    elif request.method == 'DELETE':
        return Rooms().deleteRoom(room_id)
    else:
        return {
            "error": "No such route"
        }

#Find an available room (lab, classroom, study space, etc.) at a time frame
@app.route('/API/rooms/availability', methods=['GET'])
def rooms_availability():
    if request.method == 'GET':
        return Operations().getAllAvailableRooms(request.json)
    else:
        return {
            "error": "No such route"
        }

#Find who appointed a room at a certain time
@app.route('/API/rooms/appointed', methods=['GET'])
def rooms_appointed():
    if request.method == 'GET':
        return Operations().whoAppointedRoom(request.json)
    else:
        return {
            "error": "No such route"
        }

#Give an all-day schedule for a room
@app.route('/API/rooms/schedule', methods=['GET'])
def rooms_schedule():
    if request.method == 'GET':
        return Operations().getRoomAllDaySchedule(request.json)
    else:
        return {
            "error": "No such route"
        }

@app.route('/API/room_unavailability', methods=['GET', 'POST', 'PUT'])
def room_unavail_route():
    if request.method == 'GET':
        return RoomUnavailability().getAllRoomUnavail()
    elif request.method == 'POST':
        return RoomUnavailability().insertRoomUnavail(request.json)
    elif request.method == 'PUT':
        return RoomUnavailability().updateRoomUnavail(request.json)
    else:
        return {
            "error": "No such route"
        }

@app.route('/API/room_unavailability/<int:room_unavail_id>', methods=['GET', 'DELETE'])
def room_unavail_byid_route(room_unavail_id):
    if request.method == 'GET':
        return RoomUnavailability().getRoomUnavailById(room_unavail_id)
    elif request.method == 'DELETE':
        return RoomUnavailability().deleteRoomUnavail(room_unavail_id)
        #     user_id = request.json['user_id']
        #     return RoomUnavailability().deleteRoomUnavailAuth(user_id, room_unavail_id)
    else:
        return {
            "error": "No such route"
        }

#10. Mark Unav/Av (with Auth)
@app.route('/API/room_unavailability/auth', methods=['POST'])
def room_unavail_auth_insert():
    if request.method == 'POST':
        return RoomUnavailability().insertRoomUnavailAuth(request.json)
    else:
        return {"error": "No such route"}        
@app.route('/API/room_unavailability/auth/<int:room_unavail_id>/<int:user_id>', methods=['DELETE'])
def room_unavail_auth_delete(room_unavail_id, user_id):
    if request.method == 'DELETE':
        return RoomUnavailability().deleteRoomUnavailAuth(user_id, room_unavail_id)
    else:
        return {"error": "No such route"}

@app.route('/API/buildings', methods=['GET', 'POST', 'PUT'])
def building_route():
    if request.method == 'GET':
        return Building().getAllBuildings()
    elif request.method == 'POST':
        return Building().insertBuilding(request.json)
    elif request.method == 'PUT':
        return Building().updateBuilding(request.json)
    else:
        return {
            "error": "No such route"
        }

@app.route('/API/buildings/<int:building_id>', methods=['GET', 'DELETE'])
def building_byid_route(building_id):
    if request.method == 'GET':
        return Building().getBuildingById(building_id)
    elif request.method == 'DELETE':
        return Building().deleteBuilding(building_id)
    else:
        return {
            "error": "404"
        }

@app.route('/API/invitee', methods=['GET', 'POST', 'PUT'])
def invitee_route():
    if request.method == 'GET':
        return Invitee().getAllInvitees()
    elif request.method == 'POST':
        return Invitee().insertInvitee(request.json)
    elif request.method == 'PUT':
        return Invitee().updateInvitee(request.json)
    else:
        return {
            "error": "No such route"
        }

@app.route('/API/invitee/<int:invitee_id>', methods=['GET', 'DELETE'])
def invitee_byid_route(invitee_id):
    if request.method == 'GET':
        return Invitee().getInviteeById(invitee_id)
    elif request.method == 'DELETE':
        return Invitee().deleteInvitee(invitee_id)
    else:
        return {
            "error": "404"
        }

#13a. Find busiest hours (Find top 5)
@app.route('/API/global/statistics/buesiesthours', methods=['GET'])
def global_busiesthours():
    if request.method == 'GET':
        return Operations().getBusiestHours()
    else:
        return {
            "error": "No such route"
        }

#13b. Find most booked users (Find top 10)
@app.route('/API/global/statistics/booked/users', methods=['GET'])
def global_bookedusers():
    if request.method == 'GET':
        return Operations().getMostBookedUsers()
    else:
        return {
            "error": "No such route"
        }

#13c. Find most booked rooms (Find top 10)
@app.route('/API/global/statistics/booked/rooms', methods=['GET'])
def global_bookedrooms():
    if request.method == 'GET':
        return Operations().getMostBookedRooms()
    else:
        return {
            "error": "No such route"
        }

if __name__ == '__main__':
    app.run()
