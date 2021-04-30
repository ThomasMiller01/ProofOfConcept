using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour {
    public Settings settings;
    public Map map;

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
                Vector2 position = new Vector2(Random.Range(0, this.map.dimensions.x), Random.Range(0, this.map.dimensions.y));
                Person person = new Person(colony, 0, 0, 0, (int)position.x, (int)position.y);
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
        /*// if person is already dead, do nothing
        if (person.is_dead) return;

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
        if (validate_pos)
        {
            person.pos = newPos;
        }
    }
}
