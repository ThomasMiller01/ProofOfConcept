using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour {
    public Settings settings;
    public Map map;

    public Person[] people;    

	// Use this for initialization
	void Start () {
        this.map.loadTexture();

        Dictionary<Colony, int> number_of_people = new Dictionary<Colony, int>();
        int max_number_of_people = 0;
        
        // init colonies
        for(int i = 0; i < settings.colonies.Length; i++)
        {
            Colony colony = new Colony(i, settings.colonies[i].name, settings.colonies[i].color);            
            number_of_people[colony] = settings.colonies[i].number_of_people;
            max_number_of_people += settings.colonies[i].number_of_people;
        }

        // init people               
        this.people = new Person[max_number_of_people];

        int j = 0;

        foreach (var item in number_of_people)
        {
            for (int k=0; k < item.Value; k++)
            {
                Vector2 position = new Vector2(Random.Range(0, this.map.dimensions.x), Random.Range(0, this.map.dimensions.y));
                Person person = new Person(j, item.Key, 0, 0, 0, (int)position.x, (int)position.y);
                this.people[j] = person;
                j++;
            }
        }        
    }
	
	// Update is called once per frame
	void Update () {
        this.map.draw(this.people);
    }
}
