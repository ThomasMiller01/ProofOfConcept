using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Person
{    
    public Colony colony;
    public int age;
    public int strength;
    public int reproduction_value;
    public Vector2 pos;
    public bool is_dead;

    public Person(Colony colony, int age, int strength, int reproduction_value, float x, float y)
    {        
        this.colony = colony;
        this.age = age;
        this.strength = strength;
        this.reproduction_value = reproduction_value;
        this.pos = new Vector2(x, y);
        this.is_dead = false;
    }
}
