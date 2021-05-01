using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using Utils;

public class Map : MonoBehaviour {

    public Texture2D map_texture;

    public Color32 land;
    public Color32 water;    

    [System.NonSerialized]
    public Vector2 dimensions;

    [System.NonSerialized]
    public Color32[] map_pixels;

    [System.NonSerialized]
    public Color32[] prev_map_pixels;    

    void Start()
    {
        Utils.sprite.setSprite(this.gameObject, Utils.sprite.createSprite(this.map_texture));
    }

    public void loadTexture()
    {        
        this.map_pixels = this.map_texture.GetPixels32();
        this.prev_map_pixels = this.map_pixels;

        this.dimensions = new Vector2(this.map_texture.width, this.map_texture.height);                
    }

    public void draw(List<Person> people)
    {
        Texture2D texture = new Texture2D(this.map_texture.width, this.map_texture.height);

        foreach(Person person in people)
        {
            this.map_pixels[Utils.pixels.array2dto1d(person.pos, (int)this.dimensions.x)] = person.colony.color;
        }

        texture.SetPixels32(this.map_pixels);
        
        texture.Apply();

        Utils.sprite.setSprite(this.gameObject, Utils.sprite.createSprite(texture));        
    }    

    public Color getPixel(Vector2 pos)
    {
        return this.map_pixels[Utils.pixels.array2dto1d(pos, (int)this.dimensions.x)];
    }
}
