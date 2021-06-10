using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Unity.Collections;
using Unity.Jobs;
using UnityEngine;

public class GameManager : MonoBehaviour {
    public Settings settings;
    public Map map;
    public Stats stats;

    [System.NonSerialized]
    public Person[] people;

    [System.NonSerialized]
    public Colony[] colonies;

    [System.NonSerialized]
    public Color32[] colony_colors;

    // Use this for initialization
    void Start() {
        // preload map dimensions
        this.map.loadTexture();

        this.people = new Person[(int)this.map.dimensions.x * (int)this.map.dimensions.y];
        this.colonies = new Colony[this.settings.colonies.Length];
        this.colony_colors = new Color32[this.settings.colonies.Length];

        // init colonies and people
        for (int i=0; i<this.settings.colonies.Length; i++)
        {
            Colony colony = new Colony(this.settings.colonies[i].name, this.settings.colonies[i].color);
            this.colonies[i] = colony;
            this.colony_colors[i] = colony.color;
            this.stats.colonies[i] = new Dictionary<string, float>();
            this.stats.colonies[i]["population"] = this.settings.colonies[i].number_of_people;
            this.stats.colonies_name[i] = this.settings.colonies[i].name;            

            IEnumerator<Vector2> positions = Utils.datastructure.next_pos(this.settings.colonies[i].start).GetEnumerator();

            for (int k = 0; k < this.settings.colonies[i].number_of_people; k++)
            {
                int age = (int)Random.Range(0, this.settings.strength.x);
                int strength = (int)Random.Range(this.settings.strength.x, this.settings.strength.y);
                int reproductionValue = (int)Random.Range(0, this.settings.reproductionThreshold);
                Person person = new Person()
                {
                    colony_id = i,
                    age = age,
                    strength = strength,
                    reproduction_value = reproductionValue
                };

                bool has_remaining = true;

                while (has_remaining)
                {
                    has_remaining = positions.MoveNext();

                    Vector2 pos = positions.Current;

                    bool is_water = this.map.getPixel(pos) == this.map.water;
                    bool is_valid = Utils.pixels.validatePosition(pos, new Vector2[] { new Vector2(0, this.map.dimensions.x), new Vector2(0, this.map.dimensions.y) });
                    bool is_empty = this.people[Utils.datastructure.convert2dto1d(pos, (int)this.map.dimensions.x)].Equals(default(Person));

                    if (!is_water && is_valid && is_empty)
                    {
                        this.people[Utils.datastructure.convert2dto1d(pos, (int)this.map.dimensions.x)] = person;

                        // set pixel
                        this.map.setPixel(pos, colony.color);

                        has_remaining = false;
                    }
                }
            }
        }

        this.map.draw();
    }

    // Update is called once per frame
    void Update() {
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

        Person[] people_cache = this.people.Clone() as Person[];

        // fille people shared array                
        NativeList<Person> people_shared = new NativeList<Person>(this.people.Length, Allocator.TempJob);
        people_shared.CopyFrom(this.people);

        NativeArray<Person> people_shared_cache = new NativeArray<Person>(people_cache, Allocator.TempJob);

        // fill map shared array
        NativeList<Color32> map_shared = new NativeList<Color32>(this.map.map_pixels.Length, Allocator.TempJob);
        map_shared.CopyFrom(this.map.map_pixels);

        NativeArray<Color32> colony_color_shared = new NativeArray<Color32>(this.colony_colors, Allocator.TempJob);

        // set colony stats
        NativeList<ColonyStats> colony_stats_shared = new NativeList<ColonyStats>(this.stats.colonies.Count, Allocator.TempJob);
        ColonyStats[] colony_stats = new ColonyStats[this.stats.colonies.Count];
        for (int i=0; i<this.stats.colonies.Count; i++)
        {        
            ColonyStats colonyStats = new ColonyStats() { population = 0, age = 0, strength = 0, reproduction_value = 0 };
            colony_stats[i] = colonyStats;
        }
        colony_stats_shared.CopyFrom(colony_stats);

        int population = 0;

        RenderPerson parallelRenderPerson = new RenderPerson()
        {
            people_cache = people_shared_cache,
            people = people_shared,
            map = map_shared,
            colonies = colony_color_shared,
            dimensions = this.map.dimensions,
            land = this.map.land,
            water = this.map.water,
            population = population,
            colony_stats = colony_stats_shared,
            reproductionThreshold = this.settings.reproductionThreshold,
            maxBirthCount = this.settings.maxBirthCount,
            staticPopulation = this.settings.staticPopulation,
            mutations = this.settings.mutations,
            EraseLastPos = this.settings.EraseLastPos,
            fight = this.settings.fight
        };

        // Schedule the job with one Execute per index in the results array and only 1 item per processing batch
        JobHandle handle = parallelRenderPerson.Schedule(people_shared_cache.Length, 1);

        // Wait for the job to complete
        handle.Complete();

        // copy people again
        for (int i = 0; i<people_shared.Length; i++)
        {            
            this.people[i] = people_shared[i];
        }

        // copy map pixels again        
        for (int i = 0; i < map_shared.Length; i++)
        {
            this.map.map_pixels[i] = map_shared[i];            
        }

        this.stats.population = population;
        for (int i=0; i<colony_stats_shared.Length; i++)
        {
            ColonyStats colonyStats = colony_stats_shared[i];
            this.stats.colonies[i]["population"] = colonyStats.population;
            this.stats.colonies[i]["age"] = colonyStats.age;
            this.stats.colonies[i]["strength"] = colonyStats.strength;
            this.stats.colonies[i]["reproduction_value"] = colonyStats.reproduction_value;
        }

        // copy stats

        // Free the memory allocated by the arrays
        people_shared_cache.Dispose();
        people_shared.Dispose();
        map_shared.Dispose();
        colony_color_shared.Dispose();
        colony_stats_shared.Dispose();

        // draw to the screen
        this.map.draw();
    }        
}