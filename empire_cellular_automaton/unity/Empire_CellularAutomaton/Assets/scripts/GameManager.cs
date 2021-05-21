using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour {
    public Settings settings;
    public Map map;
    public Stats stats;

    [System.NonSerialized]
    public Person[,] people;    

    // Use this for initialization
    void Start () {
        // preload map dimensions
        this.map.loadTexture();

        this.people = new Person[(int)this.map.dimensions.x, (int)this.map.dimensions.y];

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
                Person person = new Person(colony, age, strength, reproductionValue);

                IEnumerable<Vector2> positions = Utils.datastructure.next_pos(c.start);
                foreach(Vector2 pos in positions)
                {
                    // check for water
                    // check for availability
                    // check for end
                    bool is_water = this.map.getPixel(pos) == this.map.water;
                    bool is_valid = Utils.pixels.validatePosition(pos, new Vector2[] { new Vector2(0, this.map.dimensions.x), new Vector2(0, this.map.dimensions.y) });
                    bool is_empty = this.people[(int)pos.x, (int)pos.y] == null;                    

                    if (!is_water && is_valid && is_empty)
                    {
                        this.people[(int)pos.x, (int)pos.y] = person;

                        // set pixel
                        this.map.setPixel(pos, person.colony.color);

                        break;
                    }
                }                
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

        // reset statistics
        this.stats.population = 0;
        foreach (var item in this.stats.colonies)
        {
            this.stats.colonies[item.Key]["population"] = 0;
            this.stats.colonies[item.Key]["age"] = 0;
            this.stats.colonies[item.Key]["strength"] = 0;
            this.stats.colonies[item.Key]["reproduction_value"] = 0;
        }

        Person[,] people_cache = this.people.Clone() as Person[,];
        
        // render people        
        for (int x=0; x<people_cache.GetLength(0); x++)
        {
            for (int y=0; y<people_cache.GetLength(1); y++)
            {
                if (people_cache[x, y] != null) this.render_person(people_cache[x, y], new Vector2(x, y));
            }
        }

        // draw to the screen
        this.map.draw();
    }

    void render_person(Person person, Vector2 pos)
    {                
        // if person is already dead
        if (person.is_dead)
        {            
            this.people[(int)pos.x, (int)pos.y] = null;

            // set pixel to land
            this.map.setPixel(pos, this.map.land);

            return;
        }

        // if person died of age, mark person as dead and do nothing
        if (person.age > person.strength && !this.settings.staticPopulation)
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
        if (person.reproduction_value >= this.settings.reproductionThreshold && !this.settings.staticPopulation)
        {
            // create new person
            Person child = new Person(person.colony, 0, Utils.simulation.get_mutation(person.strength, this.settings.mutations), 0);

            Vector2 child_dir = Utils.pixels.getRandomDirection();
            Vector2 child_pos = Utils.pixels.getRandomNeighbour(pos, child_dir);

            // check for water
            // check is pos is valid
            // check for availability                
            bool child_is_water = this.map.getPixel(child_pos) == this.map.water;
            bool child_is_valid = Utils.pixels.validatePosition(child_pos, new Vector2[] { new Vector2(0, this.map.dimensions.x), new Vector2(0, this.map.dimensions.y) });
            bool child_is_empty = this.people[(int)child_pos.x, (int)child_pos.y] == null;

            if (!child_is_water && child_is_valid && child_is_empty)
            {
                this.people[(int)child_pos.x, (int)child_pos.y] = child;

                // set child pixel color
                this.map.setPixel(child_pos, child.colony.color);
                
                // reset person reproduction value and increase birth count
                person.reproduction_value = 0;
                person.birth_count++;
            }        
        } else
        {
            // possibility to reproduce reduces the more children a person has
            if (Random.Range(0, this.settings.maxBirthCount) >= person.birth_count)
            {
                person.reproduction_value++;
            }                            
        }
        
        // move
        // get random direction and random neighbour to move to
        Vector2 dir = Utils.pixels.getRandomDirection();
        Vector2 newPos = Utils.pixels.getRandomNeighbour(pos, dir);        

        // check, if the new position is valid
        bool is_valid = Utils.pixels.validatePosition(newPos, new Vector2[] { new Vector2(0, this.map.dimensions.x), new Vector2(0, this.map.dimensions.y) });
        
        // is water at the new position
        bool is_water = this.map.getPixel(newPos) == this.map.water;

        // are there less people at the new position
        bool is_empty = this.people[(int)newPos.x, (int)newPos.y] == null;

        // only move if
        // - its a valid position inside the world
        // - its not water
        // - there are less people than at the current position
        if (is_valid && !is_water && is_empty)
        {            
            this.people[(int)pos.x, (int)pos.y] = null;
            this.people[(int)newPos.x, (int)newPos.y] = person;

            // set color of pixel
            if (this.settings.EraseLastPos) this.map.setPixel(pos, this.map.land);
            this.map.setPixel(newPos, person.colony.color);
        }

        // if somebody else is on the field where the person wants to move
        if (!is_empty)
        {
            // get person occupying the field
            Person other = this.people[(int)newPos.x, (int)newPos.y];

            // if they are member of the same colony
            if (other.colony == person.colony)
            {
                // for now, do nothing
                // spread the disease (TODO)
            } else
            {
                if (this.settings.fight)
                {
                    // this is an enemy from another colony
                    if (person.strength == other.strength)
                    {
                        // if they have the same strength
                        // nothing happens
                    }
                    else if (person.strength > other.strength)
                    {
                        // if else the person has the greater strength
                        // the enemy dies

                        other.is_dead = true;                        
                    }
                    else
                    {
                        // if else the enemy has the greater strength
                        // the person dies
                        person.is_dead = true;                        
                    }
                }                
            }
        }

        // increase population for stats
        this.stats.population++;
        this.stats.colonies[person.colony.name]["population"]++;
        this.stats.colonies[person.colony.name]["age"] += person.age;
        this.stats.colonies[person.colony.name]["strength"] += person.strength;
        this.stats.colonies[person.colony.name]["reproduction_value"] += person.reproduction_value;
    }
    
}