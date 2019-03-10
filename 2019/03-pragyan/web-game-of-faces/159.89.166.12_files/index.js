let item1 = document.getElementById('item1')
let item2 = document.getElementById('item2')
let item3 = document.getElementById('item3')

function random_bg_color() {
    var x = Math.floor(Math.random() * 256)
    var y = Math.floor(Math.random() * 256)
    var z = Math.floor(Math.random() * 256)
    var bgColor = "rgb(" + x + "," + y + "," + z + ")"
    console.log(bgColor);
    return bgColor
}

item1.style.backgroundColor = random_bg_color()
item2.style.backgroundColor = random_bg_color()
item3.style.backgroundColor = random_bg_color()
