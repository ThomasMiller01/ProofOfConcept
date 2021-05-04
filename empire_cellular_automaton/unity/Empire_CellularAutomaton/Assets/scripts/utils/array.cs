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
    }
}