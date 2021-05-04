using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Stats : MonoBehaviour {    
    public Text generationText;
    public Text peopleText;
    public Text coloniesText;

    [System.NonSerialized]
    public int generation;
    [System.NonSerialized]
    public int year;
    [System.NonSerialized]
    public int day;
    [System.NonSerialized]
    public int population;
    [System.NonSerialized]
    public Dictionary<string, Dictionary<string, float>> colonies = new Dictionary<string, Dictionary<string, float>>();

    // Update is called once per frame
    void Update () {
        // generation
        string generation_text = "Gen [" + this.generation.ToString() + "], Year [" + this.year.ToString() + "], Day [" + this.day.ToString() + "]";
        this.generationText.text = generation_text;               

        this.peopleText.text = "Population: " + this.population.ToString();

        List<string> colonies_text = new List<string>();

        foreach(var item in this.colonies)
        {
            float population = item.Value["population"];
            float age = Mathf.Round(item.Value["age"] / item.Value["population"] / 365 * 100f) / 100f;
            float strength = Mathf.Round(item.Value["strength"] / item.Value["population"]);
            float reproduction_value = Mathf.Round(item.Value["reproduction_value"] / item.Value["population"]);
            colonies_text.Add(item.Key + ": " + population + "\n  - age: " + age + " years\n  - strength: " + strength + "\n  - reproduction_value: " + reproduction_value);
        }
        this.coloniesText.text = string.Join("\n", colonies_text.ToArray());
    }
}
