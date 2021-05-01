using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Utils
{
    public class pixels
    {
        public static int array2dto1d(Vector2 pos, int width)
        {
            return (int)pos.y * width + (int)pos.x;
        }

        public static Vector2 WorldToScreen(GameObject gameObject, Vector2 pos)
        {
            Texture2D map_texture = gameObject.GetComponent<SpriteRenderer>().sprite.texture;

            Vector2 center = new Vector2(map_texture.width / 2, map_texture.height / 2);

            // move center point to middle            
            Vector2 distances = pos - center;

            // convert world coordinates to screen coordinates
            Vector2 world = distances / 100;

            return world;
        }

        public static Vector2 getRandomNeighbour(Vector2 pos, Vector2 dir)
        {            
            Vector2 newPos = new Vector2(pos.x + dir.x, pos.y + dir.y);
            return newPos;
        }

        public static Vector2 getRandomDirection()
        {
            Vector2[] directions = new Vector2[]
            {
                new Vector2(0, 1), // top
                new Vector2(1, 0), // right
                new Vector2(0, -1), // bottom
                new Vector2(-1, 0), // left                
            };

            // return random dir
            return directions[Random.Range(0, directions.Length)];
        }
        
        public static bool validatePosition(Vector2 pos, Vector2[] boundaries)
        {
            Vector2 width = boundaries[0];
            Vector2 height = boundaries[1];

            // if the new position is outside the width area
            if (pos.x < width.x || pos.x > width.y) return false;
            
            // if the new position is outside the height area
            if (pos.y < height.x || pos.y > height.y) return false;

            return true;
        }
    }
}