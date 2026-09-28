import sys
import json
from client import BarnesHutNBody

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-barnes-hut-nbody-gravity-simulation-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "simulate_nbody_gravity",
                        "description": "Simulate gravitational N-body physics using Barnes-Hut quadtree algorithm",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "bodies": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "x": {"type": "number"}, "y": {"type": "number"},
                                            "vx": {"type": "number"}, "vy": {"type": "number"},
                                            "mass": {"type": "number"}
                                        },
                                        "required": ["x", "y", "vx", "vy", "mass"]
                                    }
                                },
                                "dt": {"type": "number", "default": 0.05},
                                "theta": {"type": "number", "default": 0.5}
                            },
                            "required": ["bodies"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "simulate_nbody_gravity":
            bodies = args.get("bodies", [])
            dt = args.get("dt", 0.05)
            theta = args.get("theta", 0.5)
            sim = BarnesHutNBody(bodies, theta=theta)
            sim.step(dt=dt)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"bodies": sim.bodies, "status": "STEP_COMPLETE"})}]
                }
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
