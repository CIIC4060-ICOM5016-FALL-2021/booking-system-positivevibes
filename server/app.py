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
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={
    r"/*": {"origins": "*"}
}, supports_credentials=True)


@app.route('/API')
def hello_world():  # put application's code here
    return 'PosVibesDB!'

@app.route('/API/users', methods=['GET', 'POST', 'PUT'])
def user_route():
    if request.method == 'GET':
        res = make_response(Users().getAllUsers())
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'POST':
        res = make_response(Users().insertUser(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'PUT':
        res = make_response(Users().updateUser(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@app.route('/API/users/<int:user_id>', methods=['GET', 'DELETE'])
def user_byid_route(user_id):
    if request.method == 'GET':
        res = make_response(Users().getUserById(user_id))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'DELETE':
        res = make_response(Users().deleteUser(user_id))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

#Give an all-day schedule for a user
@app.route('/API/users/schedule', methods=['GET'])
def user_schedule():
    if request.method == 'GET':
        res = make_response(Operations().getAllDayScheduleforUser(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

#12.a Most used Room
@app.route('/API/users/statistics/<int:user_id>/room', methods=['GET'])
def user_stat_room(user_id):
    if request.method == 'GET':
        res = make_response(Operations().getMostUsedRoom(user_id))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

#12b. User logged in user has been most booked with
@app.route('/API/users/statistics/<int:user_id>/user', methods=['GET'])
def user_stat_user(user_id):
    if request.method == 'GET':
        res = make_response(Operations().getMostBookedWithUser(user_id))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@app.route('/API/schedule', methods=['GET', 'POST', 'PUT'])
def schedule_route():
    if request.method == 'GET':
       res = make_response(Schedule().getAllSchedules())
       res.headers['Access-Control-Allow-Origin'] = '*'
       return res
    elif request.method == 'POST':
        res = make_response(Schedule().insertSchedule(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'PUT':
        res =  make_response(Schedule().updateSchedule(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@app.route('/API/schedule/<int:schedule_id>', methods=['GET', 'DELETE'])
def schedule_byid_route(schedule_id):
    if request.method == 'GET':
        res = make_response(Schedule().getScheduleById(schedule_id))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'DELETE':
        res =  make_response(Schedule().deleteSchedule(schedule_id))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

#8. Find a time that is free for everyone in the meeting
@app.route('/API/schedule/available', methods=['GET'])
def schedule_find_timeslots():
    if request.method == 'GET':
        res =  make_response(Operations().findAvailableTimeSlot(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@app.route('/API/user_unavailability', methods=['GET', 'POST', 'PUT'])
def user_unavail_route():
    if request.method == 'GET':        
        res = make_response(UserUnavailability().getAllUnavailableUsers())
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'POST':
        res = make_response(UserUnavailability().insertUnavailableUser(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'PUT':
        res =  make_response(UserUnavailability().updateUnavailableUser(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@app.route('/API/user_unavailability/<int:user_unavail_id>', methods=['GET', 'DELETE'])
def user_unavail_byid_route(user_unavail_id):
    if request.method == 'GET':
        res = make_response(UserUnavailability().getUnavailableUserById(user_unavail_id))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'DELETE':
        res = make_response(UserUnavailability().deleteUnavailableUser(user_unavail_id))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@app.route('/API/rooms', methods=['GET', 'POST', 'PUT'])
def rooms_route():
    if request.method == 'GET':
        res = make_response(Rooms().getAllRooms())
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'POST':
        res = make_response(Rooms().insertRoom(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'PUT':
        res = make_response(Rooms().updateRoom(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@app.route('/API/rooms/<int:room_id>/<int:user_id>', methods=['GET'])
def rooms_auth_route(room_id, user_id):
    if request.method == 'GET':
        res = make_response(Rooms().getRoomWithAuth(room_id, user_id))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@app.route('/API/rooms/<int:room_id>', methods=['GET', 'DELETE'])
def rooms_byid_route(room_id):
    if request.method == 'GET':
        res = make_response(Rooms().getRoomById(room_id))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'DELETE':
        res = make_response(Rooms().deleteRoom(room_id))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

#Find an available room (lab, classroom, study space, etc.) at a time frame
@app.route('/API/rooms/availability', methods=['GET'])
def rooms_availability():
    if request.method == 'GET':
        res = make_response(Operations().getAllAvailableRooms(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

#Find who appointed a room at a certain time
@app.route('/API/rooms/appointed', methods=['GET'])
def rooms_appointed():
    if request.method == 'GET':
        res = make_response(Operations().whoAppointedRoom(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

#Give an all-day schedule for a room
@app.route('/API/rooms/schedule', methods=['GET'])
def rooms_schedule():
    if request.method == 'GET':
        res = make_response(Operations().getRoomAllDaySchedule(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@app.route('/API/room_unavailability', methods=['GET', 'POST', 'PUT'])
def room_unavail_route():
    if request.method == 'GET':
        res = make_response(RoomUnavailability().getAllRoomUnavail())
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'POST':
        res = make_response(RoomUnavailability().insertRoomUnavail(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'PUT':
        res = make_response(RoomUnavailability().updateRoomUnavail(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@app.route('/API/room_unavailability/<int:room_unavail_id>', methods=['GET', 'DELETE'])
def room_unavail_byid_route(room_unavail_id):
    if request.method == 'GET':
        res = make_response(RoomUnavailability().getRoomUnavailById(room_unavail_id))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'DELETE':
        res = make_response(RoomUnavailability().deleteRoomUnavail(room_unavail_id))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

#10. Mark Unav/Av (with Auth)
@app.route('/API/room_unavailability/auth', methods=['POST'])
def room_unavail_auth_insert():
    if request.method == 'POST':
        res = make_response(RoomUnavailability().insertRoomUnavailAuth(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res        
@app.route('/API/room_unavailability/auth/<int:room_unavail_id>/<int:user_id>', methods=['DELETE'])
def room_unavail_auth_delete(room_unavail_id, user_id):
    if request.method == 'DELETE':
        res =  make_response(RoomUnavailability().deleteRoomUnavailAuth(user_id, room_unavail_id))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@app.route('/API/buildings', methods=['GET', 'POST', 'PUT'])
def building_route():
    if request.method == 'GET':
        res =  make_response(Building().getAllBuildings())
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'POST':
        res =  make_response(Building().insertBuilding(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'PUT':
        res =  make_response(Building().updateBuilding(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@app.route('/API/buildings/<int:building_id>', methods=['GET', 'DELETE'])
def building_byid_route(building_id):
    if request.method == 'GET':
        res =  make_response(Building().getBuildingById(building_id))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'DELETE':
        res =  make_response(Building().deleteBuilding(building_id))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@app.route('/API/invitee', methods=['GET', 'POST', 'PUT'])
def invitee_route():
    if request.method == 'GET':
        res = make_response(Invitee().getAllInvitees())
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'POST':
        res = make_response(Invitee().insertInvitee(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'PUT':
        res = make_response(Invitee().updateInvitee(request.json))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

@app.route('/API/invitee/<int:invitee_id>', methods=['GET', 'DELETE'])
def invitee_byid_route(invitee_id):
    if request.method == 'GET':
        res = make_response(Invitee().getInviteeById(invitee_id))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    elif request.method == 'DELETE':
        res = make_response(Invitee().deleteInvitee(invitee_id))
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

#13a. Find busiest hours (Find top 5)
@app.route('/API/global/statistics/buesiesthours', methods=['GET'])
def global_busiesthours():
    if request.method == 'GET':
        res = make_response(Operations().getBusiestHours())
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

#13b. Find most booked users (Find top 10)
@app.route('/API/global/statistics/booked/users', methods=['GET'])
def global_bookedusers():
    if request.method == 'GET':
        res = make_response(Operations().getMostBookedUsers())
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

#13c. Find most booked rooms (Find top 10)
@app.route('/API/global/statistics/booked/rooms', methods=['GET'])
def global_bookedrooms():
    if request.method == 'GET':
        res = make_response(Operations().getMostBookedRooms())
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res
    else:
        err = {"error": "No such route"}
        res = make_response(err)
        res.headers['Access-Control-Allow-Origin'] = '*'
        return res

if __name__ == '__main__':
    app.run()
