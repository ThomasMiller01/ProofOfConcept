using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using Utils;

public class Map : MonoBehaviour {

    public Texture2D map_texture;
    
    public Vector2 dimensions;

    void Start()
    {
        Utils.sprite.setSprite(this.gameObject, Utils.sprite.createSprite(this.map_texture));        
    }

    public void loadTexture()
    {
        // set map dimensions
        this.dimensions = new Vector2(this.map_texture.width, this.map_texture.height);
    }

    public void draw(List<Person> people)
    {                        
        Texture2D texture = new Texture2D(this.map_texture.width, this.map_texture.height);

        // first set original map
        for (int y = 0; y < texture.height; y++)
        {
            for (int x = 0; x < texture.width; x++)
            {
                texture.SetPixel(x, y, this.map_texture.GetPixel(x, y));
            }
        }

        // set people
        for (int i=0; i < people.Count; i++)
        {            
            texture.SetPixel((int)people[i].pos.x, (int)people[i].pos.y, people[i].colony.color);
        }        
        texture.Apply();

        Utils.sprite.setSprite(this.gameObject, Utils.sprite.createSprite(texture));        
    }    
}
