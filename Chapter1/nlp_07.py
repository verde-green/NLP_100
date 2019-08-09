# -*- cpding: utf-8 -*-

def template(x, y, z):
    return f"{x}時の{y}は{z}"

if __name__ == "__main__":
    print(template(x=12, y="気温", z=22.4))
