# `/api/items`

## `GET /`
```
# Request
None

# Response
status: 200
body: {
  success: true,
  message: "data exists",
  data: {
    itemCount: number
    itemList: [{
      pk: number,
      name: string,
      isSoldOut: boolean,
      price: number,
      image_link: string
    }...]
  }
}

```


## `GET /:pk`
```
# Request
none
# Response
status: 200
body: {
  success: true,
  message: "data exists",
  data: {
    item: {
      pk: number,
      name: string,
      isSoldOut: boolean,
      price: number,
      image_link: string
    }
  }
}

status: 404
body: {
  success: false,
  message: "data not found",
  data: {}
}
```



