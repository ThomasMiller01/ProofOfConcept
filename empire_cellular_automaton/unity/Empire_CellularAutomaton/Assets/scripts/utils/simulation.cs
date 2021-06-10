﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Utils
{
    public class simulation
    {
        public static int get_mutation(float value, bool active, int percentage=25, int add=50, int[] amount_range=null)
        {
            // calculate if amount should be added or removed
            System.Random rnd = new System.Random();

            bool do_something = rnd.Next(0, 100) < percentage;

            if (do_something && active)
            {
                // calculate if amount should be added or removed
                bool should_add = rnd.Next(0, 100) < add;
                // calculate amount
                if (amount_range == null) amount_range = new int[] { 20, 100 };
                int amount = rnd.Next(amount_range[0], amount_range[1]);

                // return value +/- amount
                if (should_add)
                {
                    return (int)(value + amount);
                }
                else
                {
                    return (int)(value - amount);
                }
            }
            else
            {
                return (int)value;
            }
        }
    }
}