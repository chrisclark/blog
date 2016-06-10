Title: Declarative Approach to Nesting Backbone Models
Date: 2013-08-01 23:57
Author: Chris Clark
Slug: declarative-approach-to-nesting
Category: Code & Tutorials

Backbone doesn't have great (any?) support for nested models. Here's my
approach. I think it's kind of fun (we get to write recursive
functions!), and hopefully useful. I'll report back when I've lived with
it for a bit longer.  
  
Here's the problem: We have a Backbone model with attributes that ought
to be other Backbone models, and some of those models' attributes ought
to also be Backbone models. We want Backbone models all the way down!
But when our REST endpoint returns data from the server, Backbone
doesn't know that and hydrates only the top-level model to a first-class
Backbone object. So we end up with ugly code inside ``_.each`` loops calling
``new App.Models.MyModel(data)`` all over the place. It's gross.
  
More concretely, after we ``fetch()``
a model (in this example, we'll use a Customer model with some nested
data), we typically get a data structure back that looks like this:

    ::coffeescript
    customer [App.Models.Customer]
      attributes : [Object]
        name : (String)
        email : (String)
        address : [Object]
        shipments : [Array]
          0 : [Object]
            date : (String)
            total : (Float)
            items : [Array]
              0 : [Object]
              1 : [Object]
          1 : [Object]
            date : (String)
            total : (Float)
            items : [Array]
              0 : [Object]
              1 : [Object]

But I actually have a bunch of Models and Collections that correspond to
various pieces of my Customer model, so what I really want is this:

    ::coffeescript
    customer : [App.Models.Customer]
      attributes : [Object]
        name : (String)
        email : (String)
        address : [App.Models.Address]
        shipments : [App.Collections.Shipments]
          models : [Array]
            0 : [App.Models.Shipment]
              attributes : [Object]
                date : (String)
                total : (Float)
                items : [App.Collections.ShipmentItems]
                  Models : [Array]
                    0 : [App.Models.ShipmentItem]
                    1 : [App.Models.ShipmentItem]
            1 : [App.Models.Shipment]
              attributes : [Object]
                date : (String)
                total : (Float)
                items : [App.Collections.ShipmentItems]
                  models : [Array]
                    0 : [App.Models.ShipmentItem]
                    1 : [App.Models.ShipmentItem]

In other words, I want to walk down my root object, and map models and
collections onto it where appropriate (we aren't trying to turn
EVERYTHING into a Backbone object, just the objects we have models and
collections for). You can of course just write a bunch of loops and do
it by hand, but I've tried to great a more general purpose method that
can be reused across an app. Basically, each model can provide a "map"
of how it should be rehydrated into a complete, nested model when it
returns from the server. So let's write that (all examples are in
Coffeescript):  

    :::coffeescript
    class App.Models.Customer extends Backbone.Model
      
      map: () ->
        [
          { name: "address", obj: App.Models.Address },
          {
            name: "shipments", obj: App.Collections.Shipments,
            children: [
              { name: "items", obj: App.Collections.ShipmentItems }
            ]
          },
        ]
  
Pretty simple! Using standard JSON we declare which attributes we want
to turn into Backbone objects, and provide an reference to the relevant
class. For deeper nesting, we just specify the child mappings in the
same manner. With this simple pattern, we can easily write arbitrarily
complex mappings, with deep nesting. Also, Backbone is helpful during
the Collection instantiation process and converts the contents of an
array into Backbone models, which is why we can stop the map at the
Collections level (although we could go deeper).  
  
Note also that map is an anonymous function, rather than just a
property. This is because we want to evaluate map at the time we hydrate
the object to ensure that all of the relevant Backbone types are
loaded.  
  
Now we need a way to walk the Customer model and apply the mapping.
We'll write a helper function called "hydrate" for that, which will
recursively walk the map and hydrate the objects:

    :::coffeescript
    App.hydrate = (root, map) =>
      if root instanceof Backbone.Model
        App.hydrate(root.attributes, map)
      else
        _.each map, (field) ->
          if field.children
            root[field.name] = App.hydrate(root[field.name], field.children)
          if _.isArray root
            _.each root, (i) -> i[field.name] = new field.obj(i[field.name])
          else
            root[field.name] = new field.obj(root[field.name])
      root
  
Let's look at this in a bit more depth because I am barely smart enough
to write recursive functions and it will give me confidence that I did
it correctly if I can explain it to you.  
  
First, if the root object is already a Backbone object, we'll walk the
attributes instead of the Model itself. This is mostly a convenience
thing so that we can call ``hydrate(model)``
instead of ``hydrate(model.attributes)``
but it also adds a bit of robustness in case you're doing something
weird and call hydrate on a model where some, but not all, of the nest
models are already Backbone objects. This'll still work and just hydrate
the ones that still need it. I don't have a guard here against
already-hydrated Collections, but it would be easy enough to add one.  
  
The function then walks through each field in the map, recursively
calling hydrate if there are any child maps present. Once we've reach
the bottom of the map, the function checks whether the object is an
array (in which case each item needs to be hydrated), or just a simple
object (in which case just the target field needs to be hydrated).  
  
This version of the function isn't tail-recursive because JavaScript VMs
don't have tail-call optimization so there's not point. It's easy to
flip the order of the field.children check though, and make it tail
recursive for [when ECMAScript 6 comes
out](http://wiki.ecmascript.org/doku.php?id=harmony:proper_tail_calls).
The tail-recursive version of the function is just a little tricker to
explain, so I opted for this one.  
  
Ok - got all that? The next step is to actually call the darn thing!
Because I'm in an auto-magical mood, we'll stick on the model's ``parse()``
method. Parse fires after every ``fetch()`` and
``save()`` of the model, so we're guaranteed to get the hydrated version back after
every server call. The full customer class thus looks like this:  

    :::coffeescript
    class App.Models.Customer extends Backbone.Model
        
      map: () ->
          ...
  
      parse: (response) ->
          App.hydrate response, @map()


And voila! Every time we sync from the server, the model will hydrate
itself! Neato!  
  
**Edit**: After writing this, I found [this
answer](http://stackoverflow.com/a/9904874/221390) on Stackoverflow,
which is very similar, and I like a lot. In some situations I like my
approach because there is a single map of the entire nesting model in
one place, on the root model, so it's very quick to get your head around
the model relationships. On the other hand, rycfung's approach is nicely
encapsulated and the parsing code is much simpler. And there is a lot to
be said for simple code when you are up late at night debugging
recursive functions.  
  
  
  
  
  
  
  

