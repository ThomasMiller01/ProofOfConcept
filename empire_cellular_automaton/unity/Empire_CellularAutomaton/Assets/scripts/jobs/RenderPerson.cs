using System.Collections;
using System.Collections.Generic;
using Unity.Collections;
using Unity.Jobs;
using UnityEngine;

public struct RenderPerson : IJobParallelFor
{
    // shared data
    [ReadOnly]
    public NativeArray<Person> people_cache;
    [NativeDisableParallelForRestriction]
    public NativeList<Person> people;
    [NativeDisableParallelForRestriction]
    public NativeList<Color32> map;
    
    public int population;
    [NativeDisableParallelForRestriction]
    public NativeList<ColonyStats> colony_stats;

    // static data
    [ReadOnly]
    public NativeArray<Color32> colonies;
    [ReadOnly]
    public Vector2 dimensions;
    [ReadOnly]
    public Color32 land;
    [ReadOnly]
    public Color32 water;

    // settings
    [ReadOnly]
    public int reproductionThreshold;
    [ReadOnly]
    public int maxBirthCount;

    [ReadOnly]
    public bool staticPopulation;
    [ReadOnly]
    public bool mutations;
    [ReadOnly]
    public bool EraseLastPos;
    [ReadOnly]
    public bool fight;


    public void Execute(int index)
    {        
        Person person = this.people_cache[index];

        if (person.Equals(default(Person))) return;        

        // if person is already dead
        if (person.is_dead)
        {
            this.people[index] = default(Person);

            // set pixel to land
            this.map[index] = this.land;

            return;
        }

        // if person died of age, mark person as dead and do nothing
        if (person.age > person.strength && !this.staticPopulation)
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
        if (person.reproduction_value >= this.reproductionThreshold && !this.staticPopulation)
        {
            // create new person
            Person child = new Person()
            {
                colony_id = person.colony_id,                
                age = 0,
                strength = Utils.simulation.get_mutation(person.strength, this.mutations),
                reproduction_value = 0
            };                

            Vector2 child_dir = Utils.pixels.getRandomDirection();
            Vector2 child_pos = Utils.pixels.getRandomNeighbour(Utils.datastructure.convert1dto2d(index, (int)this.dimensions.x), child_dir);

            // check for water
            // check is pos is valid
            // check for availability                
            bool child_is_water = this.map[Utils.datastructure.convert2dto1d(child_pos, (int)this.dimensions.x)].Equals(this.water);
            bool child_is_valid = Utils.pixels.validatePosition(child_pos, new Vector2[] { new Vector2(0, this.dimensions.x), new Vector2(0, this.dimensions.y) });
            bool child_is_empty = this.people[Utils.datastructure.convert2dto1d(child_pos, (int)this.dimensions.x)].Equals(default(Person));

            if (!child_is_water && child_is_valid && child_is_empty)
            {
                this.people[Utils.datastructure.convert2dto1d(child_pos, (int)this.dimensions.x)] = child;

                // set child pixel color
                this.map[Utils.datastructure.convert2dto1d(child_pos, (int)this.dimensions.x)] = this.colonies[child.colony_id];

                // reset person reproduction value and increase birth count
                person.reproduction_value = 0;
                person.birth_count++;
            }
        }
        else
        {
            System.Random rnd = new System.Random();

            // possibility to reproduce reduces the more children a person has
            if (rnd.Next(0, this.maxBirthCount) >= person.birth_count)
            {
                person.reproduction_value++;
            }
        }

        // move
        // get random direction and random neighbour to move to
        Vector2 dir = Utils.pixels.getRandomDirection();
        Vector2 newPos = Utils.pixels.getRandomNeighbour(Utils.datastructure.convert1dto2d(index, (int)this.dimensions.x), dir);

        // check, if the new position is valid
        bool is_valid = Utils.pixels.validatePosition(newPos, new Vector2[] { new Vector2(0, this.dimensions.x), new Vector2(0, this.dimensions.y) });

        // is water at the new position
        bool is_water = this.map[Utils.datastructure.convert2dto1d(newPos, (int)this.dimensions.x)].Equals(this.water);

        // are there less people at the new position
        bool is_empty = this.people[Utils.datastructure.convert2dto1d(newPos, (int)this.dimensions.x)].Equals(default(Person));

        // only move if
        // - its a valid position inside the world
        // - its not water
        // - there are less people than at the current position
        if (is_valid && !is_water && is_empty)
        {
            this.people[index] = default(Person);
            this.people[Utils.datastructure.convert2dto1d(newPos, (int)this.dimensions.x)] = person;

            // set color of pixel
            if (this.EraseLastPos) this.map[index] = this.land;
            this.map[Utils.datastructure.convert2dto1d(newPos, (int)this.dimensions.x)] = this.colonies[person.colony_id];
        }

        // if somebody else is on the field where the person wants to move
        if (!is_empty && !this.staticPopulation)
        {
            // get person occupying the field
            Person other = people[Utils.datastructure.convert2dto1d(newPos, (int)this.dimensions.x)];

            // if they are member of the same colony
            if (other.colony_id == person.colony_id)
            {
                // for now, do nothing
                // spread the disease (TODO)
            }
            else
            {
                if (this.fight)
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
        this.population++;

        ColonyStats colonyStats = this.colony_stats[person.colony_id];

        colonyStats.population++;
        colonyStats.age += person.age;
        colonyStats.strength += person.strength;
        colonyStats.reproduction_value += person.reproduction_value;
    }
}
