# genpark-barnes-hut-nbody-gravity-simulation-skill

Agent Skill implementing the **Barnes-Hut $O(N \log N)$ hierarchical quadtree algorithm** for gravitational N-body simulations with Multipole Acceptance Criteria (MAC).

## Architectural Overview
```mermaid
flowchart TD
    Bodies["N Point Masses"] --> Quad["Build Hierarchical Quadtree"]
    Quad --> COM["Compute Center of Mass & Total Mass per Node"]
    COM --> MAC{"Check MAC: Size / Dist < Theta ?"}
    MAC -- Yes --> Approx["Approximate Subtree as Single Point Mass"]
    MAC -- No --> Recurse["Traverse Quadtree Children"]
    Approx & Recurse --> Force["Accumulate Gravitational Force"]
    Force --> Euler["Symplectic Euler Step: Update Velocities & Positions"]
```
