alert("js агружен");
var ship_size = 1;
var flag = false;
const board = [];
var one = 4;
var two = 3;
var free = 2;
var four = 1;
var need_to_go = true;
function repeat_stuff()
{
    for (var y = 0; y < 10; y++) {
        for (var x = 0; x < 10; x++){
            document.write('<button onclick="put('+x+','+y+')", id="'+x+'_'+y+'";">🟦</button>');
        }
        document.write('<br/>');
    }
    document.write('<br/>');
    document.write('<button onclick="rotate_ship()", id="rotate";">🢂</button>');
    document.write('<button onclick="set_ship_size(4);">⬛⬛⬛⬛</button>');
    document.write('<button onclick="set_ship_size(3);">⬛⬛⬛</button>');
    document.write('<button onclick="set_ship_size(2);">⬛⬛</button>');
    document.write('<button onclick="set_ship_size(1);">⬛</button>');
    document.write('<button onclick="complete();">complete</button>');
}
function put(x, y)
{
    if (flag==false) {
    if (x + ship_size - 1 < 10) {
        for (var i = Math.max(x - 1, 0); i < Math.min(x + ship_size + 1, 9); i++) {
            if (document.getElementById(i+"_"+y).innerHTML=='⬛' ||  document.getElementById(i+"_"+Math.min(y + 1, 9)).innerHTML=='⬛' || document.getElementById(i+"_"+Math.max(y - 1, 0)).innerHTML=='⬛') {
                alert("Вы не можете разместить здесь свой корабль");
                need_to_go = false;
                break;
            }
        }
        if (need_to_go==true) {
        if (ship_size==1) {
            if (one==0) {
                alert("У вас закончились корабли этого типа");
                need_to_go=false;
            } else {
                one = one - 1;
            }
        } else if (ship_size==2) {
            if (two==0) {
                alert("У вас закончились корабли этого типа");
                need_to_go=false;
            } else {
                two = two - 1;
            }
        } else if (ship_size==3) {
            if (free==0) {
                alert("У вас закончились корабли этого типа");
                need_to_go=false;
            } else {
                free = free - 1;
            }
        } else {
            if (four==0) {
                alert("У вас закончились корабли этого типа");
                need_to_go=false;
            } else {
                four = four - 1;
            }
        }
        if (need_to_go==true) {
        for (var i = x; i < x + ship_size; i++) {
            board.push([i, y]);
            document.getElementById(i+"_"+y).innerHTML='⬛';
        }
        }
        }
    } else {
        alert("Вы не можете разместить здесь свой корабль");
    }
    } else {
        if (y + ship_size - 1 < 10) {
            for (var i = Math.max(y - 1, 0); i < Math.min(y + ship_size + 1, 9); i++) {
                if (document.getElementById(x+"_"+i).innerHTML=='⬛' ||  document.getElementById(Math.min(x + 1, 9)+"_"+i).innerHTML=='⬛' || document.getElementById(Math.max(x - 1, 0)+"_"+i).innerHTML=='⬛') {
                    alert("Вы не можете разместить здесь свой корабль");
                    need_to_go = false;
                    break;
                }
            }
            if (need_to_go==true) {
            if (ship_size==1) {
                if (one==0) {
                    alert("У вас закончились корабли этого типа");
                    need_to_go=false;
                } else {
                    one = one - 1;
                }
            } else if (ship_size==2) {
                if (two==0) {
                    alert("У вас закончились корабли этого типа");
                    need_to_go=false;
                } else {
                    two = two - 1;
                }
            } else if (ship_size==3) {
                if (free==0) {
                    alert("У вас закончились корабли этого типа");
                    need_to_go=false;
                } else {
                    free = free - 1;
                }
            } else {
                if (four==0) {
                    alert("У вас закончились корабли этого типа");
                    need_to_go=false;
                } else {
                    four = four - 1;
                }
            }
            if (need_to_go==true) {
            for (var i = y; i < y + ship_size; i++) {
                board.push([x, i]);
                document.getElementById(x+"_"+i).innerHTML='⬛';
            }
            }
            }
        } else {
            alert("Вы не можете разместить здесь свой корабль");
        }
    }
    need_to_go = true;
}
function rotate_ship()
{
    if (flag==false) {
    flag = true;
    alert("Повернули корабль, теперь он вертикальный");
    document.getElementById("rotate").innerHTML='🢃';
    } else {
    flag = false;
    alert("Повернули корабль, теперь он горизонтальный");
    document.getElementById("rotate").innerHTML='🢂';
    }
}
function set_ship_size(size) {
    ship_size = size;
    alert("Корабль длины " + size);
}
function complete() {
    if (one+two+free+four==0){
    alert("Вы расставили все корабли");
    alert(board);
    window.open("./new_game","_self");
    } else {
    alert("Закончите расстановку кораблей");
    alert(board);
    }
}
repeat_stuff();