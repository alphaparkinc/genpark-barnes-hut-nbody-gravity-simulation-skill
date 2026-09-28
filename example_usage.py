from client import BarnesHutNBody

bodies = [
    {"x": 0.0, "y": 0.0, "vx": 0.0, "vy": 1.0, "mass": 100.0},
    {"x": 10.0, "y": 0.0, "vx": 0.0, "vy": -1.0, "mass": 50.0},
    {"x": 5.0, "y": 5.0, "vx": -1.0, "vy": 0.0, "mass": 25.0}
]
sim = BarnesHutNBody(bodies, theta=0.5, G=1.0)
sim.step(dt=0.1)

print("Barnes-Hut Gravitational Step Complete:")
for i, b in enumerate(bodies):
    print(f"  Body {i+1}: pos=({b['x']:.3f}, {b['y']:.3f}) | vel=({b['vx']:.3f}, {b['vy']:.3f})")
