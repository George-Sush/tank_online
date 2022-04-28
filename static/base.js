alert("js агружен");
var ship_size = 1;
var field_size = 10
var flag = false;
available_ships = {1: 4, 2: 3, 3: 2, 4: 1}
const board = [];
var need_to_go = true;
function repeat_stuff()
{
    for (var y = 0; y < field_size; y++) {
        for (var x = 0; x < field_size; x++){
            document.write('<button onclick="put('+x+','+y+')", id="'+x+'_'+y+'";">🟦</button>');
        }
        document.write('<br/>');
    }
    document.write('<br/>');
    document.write('<button onclick="rotate_ship()", id="rotate";">🢂</button>');
    document.write('<button id="4", disabled, onclick="set_ship_size(4);">⬛⬛⬛⬛</button>');
    document.write('<button id="3", disabled, onclick="set_ship_size(3);">⬛⬛⬛</button>');
    document.write('<button id="2", disabled, onclick="set_ship_size(2);">⬛⬛</button>');
    document.write('<button id="1", disabled, onclick="set_ship_size(1);">⬛</button>');
    document.getElementById('1').disabled = false;
    document.getElementById('2').disabled = false;
    document.getElementById('3').disabled = false;
    document.getElementById('4').disabled = false;
    document.write('<button onclick="complete();">complete</button>');
    document.write('<label id="alert_label"></label>');
    document.write('<br/>');
    document.write('<button onclick="standart();">стандартная расстановка</button>')
}
function standart() {
    ship_size = 1;
    put(0, 0);
    put(0, 9);
    put(9, 0);
    put(9, 9);
    ship_size = 2;
    put(3, 0);
    put(0, 2);
    put(0, 4);
    ship_size = 3;
    put(0, 6);
    put(5, 6);
    ship_size = 4;
    put(4, 2)
}
function check_ship(x, y) {
    if (available_ships[ship_size] <= 0) return 0;
    let min_x = x - 1;
    let min_y = y - 1;
    if (flag) {
        max_x = x + 1;
        max_y = y + ship_size;
    } else {
        max_x = x + ship_size;
        max_y = y + 1;
    }
    if (x < 0 || max_x > field_size ||
        y < 0 || max_y > field_size) {
        return -1;
    }
    for (let x = min_x; x <= max_x; x++)
    for (let y = min_y; y <= max_y; y++)
    {
        if (check_place_taken(x, y)) return -2;
    }
    return 1;
}
function check_place_taken(x, y) {
    let element = document.getElementById(x+"_"+y);
    if (element && element.innerHTML == '⬛') return true;
    return false;
}
function put(x, y) {
    let check = check_ship(x, y);
    if (check > 0)
    {
        place_ship(x, y);
    } else if (check == 0) {
        document.getElementById("alert_label").innerHTML="У вас закончились корабли этого типа";
    } else {
        document.getElementById("alert_label").innerHTML="Вы не можете разместить здесь свой корабль";
    }
}
function place_ship(x, y) {
    let min_x = x;
    let min_y = y;
    if (flag) {
        max_y = y + ship_size;
    } else {
        max_x = x + ship_size;
    }
    for (var x = min_x; x < max_x; x++)
    for (var y = min_y; y < max_y; y++) {
        board.push([x, y]);
        document.getElementById(x+"_"+y).innerHTML='⬛';
    }
    available_ships[ship_size] = available_ships[ship_size] - 1
    if (available_ships[ship_size]==0) {
        document.getElementById(ship_size).disabled = true;
    }
}
function rotate_ship() {
    if (flag==false) {
    flag = true;
    document.getElementById("alert_label").innerHTML="Повернули корабль, теперь он вертикальный";
    document.getElementById("rotate").innerHTML='🢃';
    } else {
    flag = false;
    document.getElementById("alert_label").innerHTML="Повернули корабль, теперь он горизонтальный";
    document.getElementById("rotate").innerHTML='🢂';
    }
}
function set_ship_size(size) {
    ship_size = size;
    document.getElementById("alert_label").innerHTML="Корабль длины " + size;
}
function complete() {
    if (available_ships[4]+available_ships[1]+available_ships[2]
        +available_ships[3]==0) {
    document.getElementById("alert_label").innerHTML="Вы расставили все корабли";
//    alert(board);
    window.open("./new_game/"+board,"_self");
    } else {
    document.getElementById("alert_label").innerHTML="Закончите расстановку кораблей";
//    alert(board);
    }
}
repeat_stuff();