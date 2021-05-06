﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour {
    public Settings settings;
    public Map map;
    public Stats stats;

    [System.NonSerialized]
    public Dictionary<Vector2, HashSet<Person>> people;          

    // Use this for initialization
    void Start () {
        // preload map dimensions
        this.map.loadTexture();

        this.people = new Dictionary<Vector2, HashSet<Person>>();        

        // init colonies and people        
        foreach(var c in this.settings.colonies)
        {
            Colony colony = new Colony(c.name, c.color);
            this.stats.colonies[colony.name] = new Dictionary<string, float>();
            this.stats.colonies[colony.name]["population"] = c.number_of_people;
            for (int k = 0; k < c.number_of_people; k++)
            {
                int age = (int)Random.Range(0, this.settings.strength.x);                
                int strength = (int)Random.Range(this.settings.strength.x, this.settings.strength.y);
                int reproductionValue = (int)Random.Range(0, this.settings.reproductionThreshold);                
                Person person = new Person(colony, age, Utils.simulation.get_mutation(strength), Utils.simulation.get_mutation(reproductionValue), c.start.x, c.start.y);
                Utils.datastructure.add_human(person, this.people);                
            }            
        }        
    }
	
	// Update is called once per frame
	void Update () {
        // check for day
        this.stats.day++;
        if (this.stats.day == this.settings.days)
        {
            this.stats.day = 0;

            // check for year
            this.stats.year++;
            if (this.stats.year == this.settings.years)
            {
                this.stats.year = 0;
                this.stats.generation++;
            }            
        }

        List<Person> people_cache = new List<Person>();

        foreach (var item in this.people)
        {
            people_cache.AddRange(item.Value);
        }

        this.stats.population = 0;
        foreach(var item in this.stats.colonies)
        {
            this.stats.colonies[item.Key]["population"] = 0;
            this.stats.colonies[item.Key]["age"] = 0;
            this.stats.colonies[item.Key]["strength"] = 0;
            this.stats.colonies[item.Key]["reproduction_value"] = 0;
        }

        // render people        
        foreach (Person person in people_cache)
        {            
            this.render_person(person);
        }                     

        // draw to the screen
        this.map.draw(this.people);
    }

    void render_person(Person input)
    {
        Person person = new Person(input.colony, input.age, input.strength, input.reproduction_value, input.pos.x, input.pos.y, input.is_dead, input.birth_count);

        this.people[person.pos].Remove(input);
        this.people[person.pos].Add(person);                

        // if person is already dead
        if (person.is_dead)
        {
            this.people[person.pos].Remove(person);
            return;
        }

        // if person died of age, mark person as dead and do nothing
        if (person.age > person.strength)
        {
            person.is_dead = true;
            return;
        }
        else
        {
            // else increase age
            person.age++;
        }

        // if person can reproduce
        if (person.reproduction_value >= this.settings.reproductionThreshold)
        {
            person.reproduction_value = 0;
            person.birth_count++;            

            // create new person
            Person child = new Person(person.colony, 0, Utils.simulation.get_mutation(person.strength), 0, person.pos.x, person.pos.y);
            Utils.datastructure.add_human(child, this.people);            
        } else
        {
            // possibility to reproduce reduces the more children a person has
            if (Random.Range(0, this.settings.maxBirthCount) >= person.birth_count)
            {
                person.reproduction_value++;
            }                            
        }

        // TODO
        // disease

        // move
        // get random direction and random neighbour to move to
        Vector2 dir = Utils.pixels.getRandomDirection();
        Vector2 newPos = Utils.pixels.getRandomNeighbour(person.pos, dir);        

        // check, if the new position is valid
        bool validate_pos = Utils.pixels.validatePosition(newPos, new Vector2[] { new Vector2(0, this.map.dimensions.x), new Vector2(0, this.map.dimensions.y) });
        
        // is water at the new position
        bool is_water = this.map.getPixel(newPos) == this.map.water;

        // are there less people at the new position
        bool is_place = true;
        if (this.people.ContainsKey(newPos) && this.people[newPos].Count > this.people[person.pos].Count) is_place = false;        

        // only move if
        // - its a valid position inside the world
        // - its not water
        // - there are less people than at the current position
        if (validate_pos && !is_water && is_place)
        {
            this.people[person.pos].Remove(person);
            person.pos = newPos;
            Utils.datastructure.add_human(person, this.people);
        }

        // increase population for stats
        this.stats.population++;
        this.stats.colonies[person.colony.name]["population"]++;
        this.stats.colonies[person.colony.name]["age"] += person.age;
        this.stats.colonies[person.colony.name]["strength"] += person.strength;
        this.stats.colonies[person.colony.name]["reproduction_value"] += person.reproduction_value;
    }
}
