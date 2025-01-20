import pyglet

floor_layer = pyglet.graphics.Group(0)
walls_layer = pyglet.graphics.Group(1)

delver_all = pyglet.graphics.Group(10)
delver = {
    "all": delver_all,
    "head": pyglet.graphics.Group(3, parent=delver_all),
    "left_foot": pyglet.graphics.Group(0, parent=delver_all),
    "right_foot": pyglet.graphics.Group(0, parent=delver_all),
    "body": pyglet.graphics.Group(1, parent=delver_all),
    "left_hand": pyglet.graphics.Group(2, parent=delver_all),
    "right_hand": pyglet.graphics.Group(2, parent=delver_all),
}

debug = pyglet.graphics.Group(20)
