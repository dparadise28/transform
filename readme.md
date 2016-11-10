# Transform

Transform is meant as a pre and post processing tool to help remove remove boiler plate code needed for doing basic reconstructions of json objects to boost productivity. 

## Getting Started

Simply clone the repo and start using. I will soon pipify/create setuptools

### Prerequisites

Python 3 (working on backwards compatibility)

### Structure

```
	transform
		tests
			transform_test.py
			util_tests.py          # to be added 
			generic_config.json    # to be reused across tests (could find it useful to distribute to each case but for now it serves its purpose)
			test_cases
				1
					expected.json
					processed.json
					unprocessed.json
				2
					expected.json
					processed.json
					unprocessed.json
				.
				.
				.
				n
		transform_utils
			# the rest is to be determined here
			# more structure is needed to avoid bloat in any script with formatting methods but its not extremely urgent now
			val_formatt.py
		transform.py
		(other documentation and init files)
```

## Running tests

The tests definitely need more work but they're simply using pythons unittest frameworks and performing some basic checks

to run tests against existing scenarios go to the root dir of the project and run the following
```
	python -m tests.transform
```

this will run through the scenarios which are comprised of different configuration of expected input and output json's or arbitrary nesting


### Here is the result of the output given a configuration setup as included in test case 1

```
generic_config

{
	"key_delimiter": " > ",
	"val_format": {
		"currency1": "cents_as_currency",
		"currency2": "dollars_as_currency"
	},
	"loop_through_vals": {
		"products": "user > items > products",
		"swatches": "images > swatches"
	}
}

expected config structure
{
	"user_info": {
		"user_name" : "user > display_info > un",
		"first_name": "user > billing > fn",
		"last_name" : "user > billing > ln",
		"phone"     : "user > billing > phone",
		"email"     : "user > billing > email"
	},
	"cart": {
		"cart_id"   : "user > items > cart_id",
		"cart_count": "user > items > cart_count",
		"products"  : [{
			"product_id": "pid",
			"quantity"  : "qty",
			"main_img"  : "images > main_img",
			"swatches"  : ["img"],
			"images"    : "images > alt_images",
			"price"     : "price",
			"name"      : "name",
			"discount"  : {
				"cents"    : "price > discount > cents",
				"dollars"  : "price > discount > dollars",
				"currency1": "price > discount > cents",
				"currency2": "price > discount > dollars"
			}
		}]
	}
}
```

```
preprocessed    (this is the input to be restructured)

{
	"user": {
		"billing": {
			"fn"        : "first",
			"ln"        : "last",
			"phone"     : "283 342 5778",
			"email"     : "user@site.com"
		},
		"display_info": {
			"un"        : "user_name",
			"desc"      : "I am a user",
			"img"       : "http://some_url.com/img..."
		},
		"items": {
			"cart_id"   : "927543",
			"cart_count": "3",
			"products"  : [{
				"pid"  : "1123kjh4g41k",
				"qty"  : "2",
				"name" : "insert something you like here :)",
				"price": {
					"regular" : "$15.99",
					"discount": {
						"cents": 1299,
						"dollars": 12.99
					}
				},
				"images"    : {
					"main_img"  : "domain.com/main.jpg",
					"swatches"  : [{
							"color": "blue",
							"img"  : "site.com/blue_swatch"
						}, {
							"color": "green",
							"img"  : "site.com/green_swatch"
						}, {
							"color": "brown",
							"img"  : "site.com/brown_swatch"
						}
					],
					"alt_images": [
						"domain.com/blue.jpg",
						"domain.com/green.jpg",
						"domain.com/brown.jpg"
					]
				}
			}, {
				"pid"  : "1123kjh4g41k",
				"qty"  : "2",
				"name" : "insert something you like here :)",
				"price": {
					"regular" : "$15:99",
					"discount": "$12:99"
				},
				"images": {
					"main_img"  : "domain.com/main.jpg",
					"alt_images": [
						"domain.com/blue.jpg",
						"domain.com/green.jpg",
						"domain.com/brown.jpg"
					]
				}
			}, {
				"pid"  : "1123kjh4g41k",
				"qty"  : "2",
				"name" : "insert something you like here :)",
				"price": {
					"regular" : "$15:99",
					"discount": "$12:99"
				},
				"images": {
					"main_img"  : "domain.com/main.jpg",
					"alt_images": [
						"domain.com/blue.jpg",
						"domain.com/green.jpg",
						"domain.com/brown.jpg"
					]
				}
			}]
		}
	}
}


processed result given the above config
{
    "user_info": {
        "email": "user@site.com",
        "user_name": "user_name",
        "phone": "283 342 5778",
        "first_name": "first",
        "last_name": "last"
    },
    "cart": {
        "cart_id": "927543",
        "products": [
            {
                "price": {
                    "discount": {
                        "dollars": 12.99,
                        "cents": 1299
                    },
                    "regular": "$15.99"
                },
                "main_img": "domain.com/main.jpg",
                "product_id": "1123kjh4g41k",
                "swatches": [
                    "site.com/blue_swatch",
                    "site.com/green_swatch",
                    "site.com/brown_swatch"
                ],
                "images": [
                    "domain.com/blue.jpg",
                    "domain.com/green.jpg",
                    "domain.com/brown.jpg"
                ],
                "discount": {
                    "dollars": 12.99,
                    "currency1": "$12.99",
                    "currency2": "$12.99",
                    "cents": 1299
                },
                "name": "insert something you like here :)",
                "quantity": "2"
            },
            {
                "price": {
                    "discount": "$12:99",
                    "regular": "$15:99"
                },
                "main_img": "domain.com/main.jpg",
                "product_id": "1123kjh4g41k",
                "swatches": [],
                "images": [
                    "domain.com/blue.jpg",
                    "domain.com/green.jpg",
                    "domain.com/brown.jpg"
                ],
                "discount": {
                    "dollars": "",
                    "currency1": null,
                    "currency2": null,
                    "cents": ""
                },
                "name": "insert something you like here :)",
                "quantity": "2"
            },
            {
                "price": {
                    "discount": "$12:99",
                    "regular": "$15:99"
                },
                "main_img": "domain.com/main.jpg",
                "product_id": "1123kjh4g41k",
                "swatches": [],
                "images": [
                    "domain.com/blue.jpg",
                    "domain.com/green.jpg",
                    "domain.com/brown.jpg"
                ],
                "discount": {
                    "dollars": "",
                    "currency1": null,
                    "currency2": null,
                    "cents": ""
                },
                "name": "insert something you like here :)",
                "quantity": "2"
            }
        ],
        "cart_count": "3"
    }
}
```


# TODO

* **Testing** (add test cases and create small unit tests for the built in formatting and transforms)
* Refactor the implementation for nested remodelling to remove the need to recurse objects (an explanation can be found in the doc string of the method itself)
* allow for additional functionality to be passed in if a non existing method is desired when formatting given current functionality (can be easily done during initiation)
* hash out plans for storing and accessing utils and tools inside transform (try to keep things dynamic in the process)
* dsl/config structure updates (along with respective code enhancements) to not allow for key collisions
* allow multiple lists to be specified in config for single value (useful in different types of aggregations)
* utilize setup tools and make pip-able
* think of debugging approaches (a lot of the above will help)
* check for backwards compatibility and tweak where needed
* benchmarks