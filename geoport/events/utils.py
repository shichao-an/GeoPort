ALPHABETS = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
MAP_PIN_SHADOW = "https://chart.googleapis.com/chart?chst="
MAP_PIN_SHADOW += "d_map_pin_letter_withshadow&chld={letter}%7CFE7569%7C000000"


def get_markers(event):
    """Generate markers for participants of a event"""
    users = event.visible_users
    markers = [
        {
            'name': user.name,
            'image': user.avatar,
            'url': user.get_absolute_url(),
            'lat': user.location[0],
            'lon': user.location[1],
        } for user in users
    ]
    for i, marker in enumerate(markers):
        marker['pin'] = MAP_PIN_SHADOW.format(letter=ALPHABETS[i])

    return markers
