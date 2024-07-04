let game_name = ''
let p1 = ''
let p2 = ''
let current_player = p1
let p1_suit = 0
let game_id = -1
let table_id = -1
let shot_id = -1
let shot_start = 0
let current_time = 0
let shot_time = 0
let last_shot_end = 0

new_game()

function new_cue_ball() {
    $.ajax({
        url: "/new_cue",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            table: table_id
        }),
        success: function(response) {
            table_id = response.table_id
            print_table(response.svg)
        },
        error: function(error) {
            console.log(error)
        }
    })
}

async function new_game() {
    p1_suit = 0
    game_id = -1
    table_id = -1
    shot_id = -1
    shot_start = 0
    current_time = 0
    shot_time = 0
    last_shot_end = 0

    p1 = window.prompt("Enter the name of Player 1", "player1")
    if (p1 == null) {
        p1 = 'player1'
    }
    p2 = window.prompt("Enter the name of Player 2", "player2")
    if (p2 == null) {
        p2 = 'player2'
    }
    game_name = window.prompt("Enter the name of the game", "game1")
    if (game_name == null) {
        game_name = 'game'
    }
    create_new_game()
    let random_num = Math.floor(Math.random() * 2)
    if ((random_num % 2) == 0) {
        current_player = p1
    } else {
        current_player = p2
    }
    update_player_text()
    setTimeout(function() {
        $('#b0').on("mousedown", (event) => create_line(event))
    }, 50)
    
}

function create_new_game() {
    $.ajax({
        url: "/new_game",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            game_name: game_name,
            player1: p1,
            player2: p2
        }),
        success: function(response) {
            game_id = response.game_id
            table_id = response.table_id
            print_table(response.svg)
        },
        error: function(error) {
            console.log(error)
        }
    })
}

function create_line(event) {
    const cue_ball = $('#b0')
    const ball_x = cue_ball.attr("cx")
    const ball_y = cue_ball.attr("cy")
    let line = document.createElementNS('http://www.w3.org/2000/svg', 'line')
    line.setAttribute('id', 'shot_line')
    $('#svg').append(line)
    line = $('#shot_line')
    line.attr('x1', ball_x)
    line.attr('y1', ball_y)
    line.attr('x2', event.clientX * (2.2) - 260)
    line.attr('y2', event.clientY * (2.214) - 120)
    line.attr('stroke', 'black')
    line.attr('stroke-width', '10')
    $('#svg').append(line)

    $('#b0').on("mousedown", () => {})
    document.onmousemove = (event) => update_line(event)
    document.onmouseup = (event) => release(event)
}

function update_line(event) {
    const line = $('#shot_line')
    line.attr('x2', event.clientX * (2.2) - 260)
    line.attr('y2', event.clientY * (2.214) - 120)
}

function release() {
    document.onmousemove = () => {}
    document.onmouseup = () => {}
    const line = $('#shot_line')
    const start_x = line.attr('x1')
    const start_y = line.attr('y1')
    const final_x = line.attr('x2')
    const final_y = line.attr('y2')
    line.remove()
    let vel_x = -10 * (final_y - start_y)
    if (vel_x > 10000) {
        vel_x = 10000
    } else if (vel_x < -10000) {
        vel_x = -10000
    }
    let vel_y = (-10) * (final_x - start_x)
    if (vel_y > 10000) {
        vel_y = 10000
    } else if (vel_y < -10000) {
        vel_y = -10000
    }
    make_shot(vel_x, vel_y)
}

function make_shot(vel_x, vel_y) {
    let ball_before = get_num_balls(current_player)
    $.ajax({
        type: "POST",
        url: "/make_shot",
        contentType: "application/json",
        data: JSON.stringify({
            game_id: game_id,
            table_id: table_id,
            player: current_player,
            x: vel_x,
            y: vel_y
        }),
        success: function(response) {
            shot_id = response.shot_id
            shot_time = response.shot_time
            shot_time
            shot_start = Date.now()
            run_animation(ball_before)
        },
        error: function(error) {
            console.log(error)
        }
    })
    
}

function run_animation(ball_before) {
    setTimeout(() => {
        current_time = (Math.floor((Date.now() - shot_start) / 10) / 100) + last_shot_end
    
        if (current_time <= shot_time) {
            fetch_table_svg(current_time)
            run_animation(ball_before)
        } else {
            fetch_table_svg(shot_time)
            more_game(ball_before)
        }
    }, 10)
}

async function fetch_table_svg(time) {
    $.ajax({
        url: "/run_animation",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({
            current_time: time,
            shot_id: shot_id
        }),
        success: function(response) {
            table_id = response.table_id
            print_table(response.svg)
        },
        error: function() {
        }
    })
}

function print_table(svg_text) {
    $("#table").remove()

    let svgdiv = document.createElement('div')
    svgdiv.setAttribute('id', 'table')
    svgdiv.innerHTML = svg_text
    $('#tableDiv').append(svgdiv)
    if (!p1_suit) {
        if ($(".high").length < 7) {
            p1_suit = 1
        } else if ($(".low").length < 7) {
            p1_suit = -1
        }
    }
}

function more_game(ball_before) {
    setTimeout(function() {
        if ($('#b8').length <= 0) {
            end_game()
            return
        }
        if ($('#b0').length <= 0) {
            new_cue_ball()
        }
        if (get_num_balls(current_player) == ball_before ) {
            switch_players()
        }
        setTimeout(() => {
            $('#b0').on("mousedown", (event) => create_line(event))
            update_player_text()
        }, 50)
        last_shot_end = shot_time
    }, 100)
}

function end_game() {
    let winner
    if (get_num_balls(current_player) == 0) {
        winner = current_player
    } else {
        if (current_player == p1) {
            winner = p2
        } else {
            winner = p1
        }
    }
    $('#currentPlayer').text(winner + " wins!")
}

function switch_players() {
    if (current_player == p1) {
        current_player = p2
        
    } else {
        current_player = p1
    }
    
}

function get_num_balls(player) {
    if (p1_suit == 1) {
        if (player == p1) {
            return $(".high").length
        } else {
            return $(".low").length
        }
    } else if (p1_suit == -1) {
        if (player == p1) {
            return $(".low").length
        } else {
            return $(".high").length
        }
    } else {
        return -1
    }
}

function update_player_text() {
    console.log(current_player + p1_suit)
    let text = "Current Player: " + current_player
    if (p1_suit == 0) {
    } else if (p1_suit == 1) {
        if (current_player == p1) {
            text += " (high balls)"
        } else {
            text += " (low balls)"
        }
    } else if (p1_suit == -1) {
        if (current_player == p1) {
            text += " (low balls)"
        } else {
            text += " (high balls)"
        }
    }

    $("#currentPlayer").text(text)
}
