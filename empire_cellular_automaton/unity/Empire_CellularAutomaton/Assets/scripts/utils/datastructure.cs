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

        public static void add_human(Person human, Dictionary<Vector2, HashSet<Person>> people)
        {
            if (!people.ContainsKey(human.pos)) people[human.pos] = new HashSet<Person>();
            people[human.pos].Add(human);
        }
    }
}