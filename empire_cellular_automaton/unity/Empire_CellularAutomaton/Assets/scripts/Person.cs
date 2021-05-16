using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Person
{    
    public Colony colony;
    public int age;
    public int strength;
    public int reproduction_value;    
    public bool is_dead;
    public int birth_count;

    public Person(Colony colony, int age, int strength, int reproduction_value, bool is_dead=false, int birth_count=0)
    {        
        this.colony = colony;
        this.age = age;
        this.strength = strength;
        this.reproduction_value = reproduction_value;        
        this.is_dead = is_dead;
        this.birth_count = birth_count;
    }
}
