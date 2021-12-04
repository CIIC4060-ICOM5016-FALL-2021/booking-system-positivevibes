
const numbers = {
    "0": "Jan",
    "1": "Feb",
    "3": "Mar",
    "4": "Apr",
    "5": "May",
    "6": "Jun",
    "7": "Jul",
    "8": "Aug",
    "9": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec",

}
const months = {
    "Jan" : "0",
    "Feb" : "1",
    "Mar" : "2",
    "Apr" : "3",
    "May" : "4",
    "Jun" : "5",
    "Jul" : "6",
    "Aug" : "7",
    "Sep" : "8",
    "Oct" : "9",
    "Nov" : "10",
    "Dec" : "11"
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
