using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Person
{
    public int id;
    public Colony colony;
    public int age;
    public int strength;
    public int reproduction_value;
    public Vector2 pos;
    public bool is_dead;

    public Person(int id, Colony colony, int age, int strength, int reproduction_value, int x, int y)
    {
        this.id = id;
        this.colony = colony;
        this.age = age;
        this.strength = strength;
        this.reproduction_value = reproduction_value;
        this.pos = new Vector2(x, y);
        this.is_dead = false;
    }
}
