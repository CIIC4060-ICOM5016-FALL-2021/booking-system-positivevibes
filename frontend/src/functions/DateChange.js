
const numbers = {
    "01": "Jan",
    "02": "Feb",
    "03": "Mar",
    "04": "Apr",
    "05": "May",
    "06": "Jun",
    "07": "Jul",
    "08": "Aug",
    "09": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec",

}
const months = {
    "Jan" : "01",
    "Feb" : "02",
    "Mar" : "03",
    "Apr" : "04",
    "May" : "05",
    "Jun" : "06",
    "Jul" : "07",
    "Aug" : "08",
    "Sep" : "09",
    "Oct" : "10",
    "Nov" : "11",
    "Dec" : "12"
}

function monthToNumber(month) {
    return months[month]
}

function numberToMonth(number) {
    return numbers[number]
    
}

export function parseFromDate(start, end) {
    // From Wed Jun 01 2022 01:30:00 GMT-0400 (Bolivia Time)
    // And Wed Jun 01 2022 03:00:00 GMT-0400 (Bolivia Time)
    // To 2022-01-01, 01:30:00, 03:00:00
    let res = [];
    start = start.toString();
    end = end.toString();
    let lines = start.split(" ");
    let date = lines[3] + '-' + monthToNumber(lines[1]) + '-' + lines[2];
    let start_time = lines[4];
    let end_time = end.split(" ")[4];
    res.push(date); 
    res.push(start_time); 
    res.push(end_time);
    return res
}

export function parseToDate(date) {

}
