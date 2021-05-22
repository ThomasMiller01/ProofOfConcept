using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Utils
{
    public class datastructure
    {
        public static int convert2dto1d(Vector2 pos, int width)
        {
            return (int)pos.y * width + (int)pos.x;
        }

        public static IEnumerable<Vector2> next_pos(Vector2 center)
        {
            int max_radius = 50;

            for (int radius=0; radius<max_radius; radius++)
            {
                int distance = radius;

                Vector2 initial = new Vector2(center.x + distance, center.y);
                Vector2 current = initial;

                int direction = 0;
                Dictionary<int, Vector2> steps = new Dictionary<int, Vector2>();
                steps.Add(0, new Vector2(0, 1));
                steps.Add(1, new Vector2(-1, 1));
                steps.Add(2, new Vector2(-1, 0));
                steps.Add(3, new Vector2(-1, -1));
                steps.Add(4, new Vector2(0, -1));
                steps.Add(5, new Vector2(1, -1));
                steps.Add(6, new Vector2(1, 0));
                steps.Add(7, new Vector2(1, 1));

                int nsteps = steps.Count;

                while (true)
                {
                    if (distance == 0)
                    {
                        yield return current;
                        break;
                    }

                    Vector2 next = new Vector2(current.x + steps[direction].x, current.y + steps[direction].y);

                    if (chebyshev_metric(center, next) != distance)
                    {
                        direction = (direction + 1) % nsteps;
                        continue;
                    }

                    yield return current;

                    current = next;
                    if (current == initial) break;
                }
            }            
        }

        private static float chebyshev_metric(Vector2 p1, Vector2 p2)
        {
            return Math.Max(Math.Abs(p1.x - p2.x), Math.Abs(p1.y - p2.y));
        }
    }
}