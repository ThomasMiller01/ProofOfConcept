using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using Utils;

public class Map : MonoBehaviour {

    public Texture2D original_map_texture;

    public Color32 land;
    public Color32 water;

    public Settings settings;    

    [System.NonSerialized]
    public Vector2 dimensions;

    [System.NonSerialized]
    public Color32[] map_pixels;

    [System.NonSerialized]
    public Texture2D map_texture;

    [System.NonSerialized]
    SpriteRenderer spriteRenderer;

    void Start()
    {        
        this.spriteRenderer = this.gameObject.GetComponent<SpriteRenderer>();
        this.spriteRenderer.sprite = Utils.sprite.createSprite(this.original_map_texture);
    }

    public void loadTexture()
    {        
        // set start pixels and dimensions
        this.map_pixels = this.original_map_texture.GetPixels32();                
        this.dimensions = new Vector2(this.original_map_texture.width, this.original_map_texture.height);

        // set texture to work with
        this.map_texture = new Texture2D((int)this.dimensions.x, (int)this.dimensions.y);
        this.map_texture.filterMode = FilterMode.Point;
    }

    public void draw()
    {
        this.map_texture.SetPixels32(this.map_pixels);                
        
        this.map_texture.Apply();

        this.spriteRenderer.sprite = Utils.sprite.createSprite(this.map_texture);
    }    

    public Color getPixel(Vector2 pos)
    {
        return this.map_pixels[Utils.datastructure.convert2dto1d(pos, (int)this.dimensions.x)];
    }

    public void setPixel(Vector2 pos, Color32 color)
    {
        this.map_pixels[Utils.datastructure.convert2dto1d(pos, (int)this.dimensions.x)] = color;
    }
}
