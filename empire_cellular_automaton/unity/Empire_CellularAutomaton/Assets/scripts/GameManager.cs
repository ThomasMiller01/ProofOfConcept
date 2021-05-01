using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour {
    public Settings settings;
    public Map map;

    [System.NonSerialized]
    public List<Person> people;      

	// Use this for initialization
	void Start () {
        // preload map dimensions
        this.map.loadTexture();

        this.people = new List<Person>();

        // init colonies and people        
        foreach(var c in this.settings.colonies)
        {
            Colony colony = new Colony(c.name, c.color);
            for (int k = 0; k < c.number_of_people; k++)
            {                
                Person person = new Person(colony, 0, 0, 0, c.start.x, c.start.y);
                this.people.Add(person);                
            }            
        }
    }
	
	// Update is called once per frame
	void Update () {
        foreach (Person person in this.people)
        {
            this.render_person(person);
        }
        this.map.draw(this.people);
    }

    void render_person(Person person)
    {
        /*// if person is already dead
        if (person.is_dead)
        {
            this.people.Remove(person);
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

            // TODO
            // mutations

            // create new person
            Person child = new Person(person.colony, 0, person.strength, 0, person.pos.x, person.pos.y);
            this.people.Add(child);
            this.map.setPerson(child);
        } else
        {
            person.reproduction_value++;
        }*/

        // TODO
        // disease

        // move
        // get random direction and random neighbour to move to
        Vector2 dir = Utils.pixels.getRandomDirection();
        Vector2 newPos = Utils.pixels.getRandomNeighbour(person.pos, dir);        

        // check, if the new position is valid
        bool validate_pos = Utils.pixels.validatePosition(newPos, new Vector2[] { new Vector2(0, this.map.dimensions.x), new Vector2(0, this.map.dimensions.y) });
        bool is_water = this.map.getPixel(newPos) == this.map.water;        

        // if its a valid position and not water, move
        if (validate_pos && !is_water)
        {                        
            person.pos = newPos;            
        }
    }
}
