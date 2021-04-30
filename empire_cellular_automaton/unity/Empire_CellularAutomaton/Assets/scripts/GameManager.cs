using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour {
    public Settings settings;
    public Map map;

    public Person[] people;
    public Colony[] colonies;

	// Use this for initialization
	void Start () {
        this.colonies = new Colony[settings.colonies.Length];

        Dictionary<int, int> number_of_people = new Dictionary<int, int>();
        int max_number_of_people = 0;
        
        // init colonies
        for(int i = 0; i < settings.colonies.Length; i++)
        {
            Colony colony = new Colony(i, settings.colonies[i].name, settings.colonies[i].color);
            this.colonies[i] = colony;
            number_of_people[i] = settings.colonies[i].number_of_people;
            max_number_of_people += settings.colonies[i].number_of_people;
        }

        // init people               
        this.people = new Person[max_number_of_people];

        int j = 0;

        foreach (var item in number_of_people)
        {
            for (int k=0; k < item.Value; k++)
            {
                Person person = new Person(j, item.Key, 0, 0, 0, 0, 0);
                this.people[j] = person;
            }
        }

        // initially draw all people
        this.map.draw(this.people);
    }
	
	// Update is called once per frame
	void Update () {
		
	}
}
