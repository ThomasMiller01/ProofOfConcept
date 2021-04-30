using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Person
{
    public int id;
    public int colony_id;
    public int age;
    public int strength;
    public int reproduction_value;
    public Vector2 pos;
    public bool is_dead;

    public Person(int id, int colony_id, int age, int strength, int reproduction_value, int x, int y)
    {
        this.id = id;
        this.colony_id = colony_id;
        this.age = age;
        this.strength = strength;
        this.reproduction_value = reproduction_value;
        this.pos = new Vector2(x, y);
        this.is_dead = false;
    }
}
