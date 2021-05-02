using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraMovement : MonoBehaviour {
    // zoom
    private float targetOrtho;
    public float zoomSpeed = 1;    
    public float smoothSpeed = 2.0f;
    public float minOrtho = 0.1f;
    private float maxOrtho;

    // movement
    public float moveSpeed = 0.1f;
    private Vector3 dragOrigin;
    private Vector3 clickOrigin = Vector3.zero;
    private Vector3 basePos = Vector3.zero;

    void Start()
    {
        this.targetOrtho = Camera.main.orthographicSize;
        this.maxOrtho = this.targetOrtho;
    }

    void Update()
    {
        this.zoom();
        this.movement();
    }

    private void zoom()
    {
        float scroll = Input.GetAxis("Mouse ScrollWheel");
        if (scroll != 0.0f)
        {
            this.targetOrtho -= scroll * this.zoomSpeed * (this.targetOrtho / 2);
            this.targetOrtho = Mathf.Clamp(this.targetOrtho, this.minOrtho, this.maxOrtho);
        }

        Camera.main.orthographicSize = Mathf.MoveTowards(Camera.main.orthographicSize, this.targetOrtho, this.smoothSpeed * Time.deltaTime);
    }

    private void movement()
    {
        float move = (this.targetOrtho * this.moveSpeed) / 100;        

        if (Input.GetMouseButtonDown(2)) {
            if (this.clickOrigin == Vector3.zero)
            {
                this.clickOrigin = Input.mousePosition;
                this.basePos = transform.position;
            }            
        }

        this.dragOrigin = Input.mousePosition;

        if (!Input.GetMouseButton(2)) {
            this.clickOrigin = Vector3.zero;
            return;
        }

        float x = basePos.x + ((this.clickOrigin.x - this.dragOrigin.x) * move);
        float y = this.basePos.y + ((this.clickOrigin.y - this.dragOrigin.y) * move);

        transform.position = new Vector3(x, y, -10);
    }
}