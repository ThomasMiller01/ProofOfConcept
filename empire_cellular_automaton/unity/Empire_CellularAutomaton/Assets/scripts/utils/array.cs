using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Utils
{
    public class array
    {
        public static int convert2dto1d(Vector2 pos, int width)
        {
            return (int)pos.y * width + (int)pos.x;
        }

        public static Dictionary<Vector2, HashSet<Person>> copy_population(Dictionary<Vector2, HashSet<Person>> people)
        {            
            Dictionary<Vector2, HashSet<Person>> copied_dict = new Dictionary<Vector2, HashSet<Person>>();

            foreach (var item in people)
            {                
                copied_dict[item.Key] = new HashSet<Person>(item.Value);
            }
            return copied_dict;
        }
    }
}