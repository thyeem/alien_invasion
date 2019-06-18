package main

import (
    "testing"
)

func Test_Parse_world_map(t *testing.T) {
    world_map := parse_world_map("../worldmap/basic.txt")
    foo, foo_ok := world_map["Foo"]
    bar, bar_ok := world_map["Bar"]

    if !foo_ok || !bar_ok {
        t.Error("not found: Foo, Bar")
    }
    foo_ok = foo["north"] == "Bar" || foo["west"] == "Baz" || foo["south"] == "Qu-ux"
    bar_ok = bar["south"] == "Foo" || bar["west"] == "Bee"

    if !foo_ok || !bar_ok {
        t.Error("wrong result")
    }
}

func Test_Init_alien_invasion(t *testing.T) {
    roads := Roads{"north": "mars"}
    world_map := WorldMap{"venus": roads}
    alien_spot := init_alien_invasion(1, world_map)
    for city, intruders := range alien_spot {
        // should initally be in venus only
        if city != "venus" {
            t.Error("wrong result")
        }
        result, ok := intruders[1]
        if !result || !ok {
            t.Error("wrong result")
        }
    }
}

func Test_Wander_randomly(t *testing.T) {
    world_map := WorldMap{
        "venus": Roads{"north": "mars"},
        "mars": Roads{"south": "venus"},
    }
    alien_spot := AlienSpot{ "venus": Intruders{1: true}, }
    wander_randomly(world_map, alien_spot)

    for city, intruders := range alien_spot {
        // should be detected in mars only
        if city != "mars" {
            t.Error("wrong result")
        }
        result, ok := intruders[1]
        if !result || !ok {
            t.Error("wrong result")
        }
    }
}

func Test_Destroy_and_kill(t *testing.T) {
    world_map := WorldMap{
        "venus": Roads{"north": "mars", "east": "earth"},
        "mars": Roads{"south": "venus"},
    }
    alien_spot := AlienSpot{ "mars": Intruders{1: true, 2: true}, }
    destroy_and_kill(world_map, alien_spot)

    for city, _ := range world_map {
        // should be venus only
        if city != "venus" {
            t.Error("wrong result")
        }
        if len(alien_spot) != 0 {
            t.Error("wrong result")
        }
    }

    for direction, vicinity := range world_map["venus"] {
        // after being destroyed, 
        // the remaining world map is "venus east=earth" only
        if direction != "east" {
            t.Error("wrong result")
        }
        if vicinity != "earth" {
            t.Error("wrong result")
        }
    }
}

