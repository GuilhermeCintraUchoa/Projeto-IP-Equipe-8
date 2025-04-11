from platform_andrews import Platform
from enemy import Enemy

def construir_fase(fase_numero):
    platforms = []
    enemies = []

    if fase_numero == 1:
        platforms.append(Platform(200, 350, 200, 20))
        platforms.append(Platform(450, 250, 200, 20))
        platforms.append(Platform(130, 150, 200, 20))

        enemies.append(Enemy(130, 100, 130, 370, 1))
        enemies.append(Enemy(450, 200, 450, 700, 1))

    elif fase_numero == 2:
        platforms.append(Platform(200, 350, 200, 20))
        platforms.append(Platform(450, 250, 20, 20))
        platforms.append(Platform(350, 200, 20, 20))
        platforms.append(Platform(600, 200, 200, 20))
        platforms.append(Platform(100, 200, 100, 20))

        enemies.append(Enemy(600, 400, 0, 850, 1))
        enemies.append(Enemy(100, 150, 100, 250, 1))
        enemies.append(Enemy(600, 150, 600, 850, 1))
    
    else:
        return None, None

    return platforms, enemies
