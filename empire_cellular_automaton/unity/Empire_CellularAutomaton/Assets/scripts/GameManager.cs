using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour {
    public Settings settings;
    public Map map;

    [System.NonSerialized]
    public Dictionary<Vector2, HashSet<Person>> people;

    [System.NonSerialized]
    public Dictionary<Vector2, HashSet<Person>> people_cache;    

    [System.NonSerialized]
    public int day;

    [System.NonSerialized]
    public int year;

    [System.NonSerialized]
    public int generation;    

    // Use this for initialization
    void Start () {
        // preload map dimensions
        this.map.loadTexture();

        this.people = new Dictionary<Vector2, HashSet<Person>>();
        this.people_cache = new Dictionary<Vector2, HashSet<Person>>();

        // init colonies and people        
        foreach(var c in this.settings.colonies)
        {
            Colony colony = new Colony(c.name, c.color);
            for (int k = 0; k < c.number_of_people; k++)
            {
                int age = (int)Random.Range(0, this.settings.strength.y);
                int strength = (int)Random.Range(this.settings.strength.x, this.settings.strength.y);
                int reproductionValue = (int)Random.Range(0, this.settings.reproductionThreshold);
                Person person = new Person(colony, age, strength, reproductionValue, c.start.x, c.start.y);
                if (!this.people.ContainsKey(person.pos)) this.people[person.pos] = new HashSet<Person>();
                this.people[person.pos].Add(person);                
            }            
        }
        this.people_cache = Utils.array.copy_population(this.people);
    }
	
	// Update is called once per frame
	void Update () {
        // check for day
        this.day++;
        if (this.day == this.settings.days)
        {
            this.day = 0;

            // check for year
            this.year++;
            if (this.year == this.settings.years)
            {
                this.year = 0;
                this.generation++;
            }            
        }                

        // render people
        foreach (var item in this.people)
        {
            foreach (Person person in item.Value)
            {
                this.render_person(person);
            }
        }

        // remove dead people
        foreach (var item in this.people_cache)
        {
            item.Value.RemoveWhere(elem => elem.is_dead);            
        }

        this.people = Utils.array.copy_population(this.people_cache);

        // draw to the screen
        this.map.draw(this.people);
    }

    void render_person(Person input)
    {
        Person person = new Person(input.colony, input.age, input.strength, input.reproduction_value, input.pos.x, input.pos.y, input.is_dead, input.birth_count);

        this.people_cache[person.pos].Remove(input);
        this.people_cache[person.pos].Add(person);                

        // if person is already dead
        if (person.is_dead)
        {            
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

            // TODO
            // mutations

            // create new person
            Person child = new Person(person.colony, (int)Random.Range(0, this.settings.strength.x), person.strength, 0, person.pos.x, person.pos.y);
            if (!this.people_cache.ContainsKey(child.pos)) this.people_cache[child.pos] = new HashSet<Person>();
            this.people_cache[child.pos].Add(child);            
        } else
        {
            // if a person is not alone, the possibility to reproduce is smaller                        
            bool is_alone = true;
            if (is_alone)
            {
                if (Random.Range(0, this.settings.maxBirthCount) >= person.birth_count)
                {
                    person.reproduction_value++;
                }                
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
        if (this.people_cache.ContainsKey(newPos) && this.people_cache[newPos].Count > this.people_cache[person.pos].Count) is_place = false;        

        // only move if
        // - its a valid position inside the world
        // - its not water
        // - there are less people than at the current position
        if (validate_pos && !is_water && is_place)
        {
            this.people_cache[person.pos].Remove(person);
            person.pos = newPos;
            if (!this.people_cache.ContainsKey(person.pos)) this.people_cache[person.pos] = new HashSet<Person>();
            this.people_cache[person.pos].Add(person);
        }
    }
}
