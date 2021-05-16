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
        
        public static IEnumerable<Vector2> next_pos(Vector2 pos)
        {
            int radius = 0;            
            for (int i = 0; i < 1000; i++)
            {
                int randX = UnityEngine.Random.Range(-radius, radius);
                int randY = UnityEngine.Random.Range(-radius, radius);

                int newX = (int)pos.x + randX;
                int newY = (int)pos.y + randY;

                if (i % 10 == 0) radius++;

                yield return new Vector2(newX, newY);                                
            }            
        }
    }
}