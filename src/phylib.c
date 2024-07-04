#include "phylib.h"

// Constructors
 
/**
* Creates and returns a new phylib_coord object with values from the 
* parameters.
*/
phylib_coord phylib_new_coord( double x, double y ) {
    phylib_coord new_coord;
    new_coord.x = x;
    new_coord.y = y;
    return new_coord; 
}

/**
* Creates and returns a new phylib_still_ball object with values from the 
* parameters. Returns NULL if memory could not be allocated or invalid 
* arguments were entered.
*/
phylib_object *phylib_new_still_ball( unsigned char number,
                                      phylib_coord * pos ) {
    if ( !pos ) {
        return NULL;
    }
    phylib_object *new_object = (phylib_object*) malloc( sizeof( phylib_object ) );
    if ( !new_object ) {
        return NULL;
    }
    new_object->type = PHYLIB_STILL_BALL;
    new_object->obj.still_ball.number = number;
    new_object->obj.still_ball.pos = *pos;
    return (phylib_object*) new_object;
}

/**
* Creates and returns a new phylib_rolling_ball object with values from the 
* parameters. Returns NULL if memory could not be allocated or invalid 
* arguments were entered.
*/
phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos
                                      , phylib_coord *vel, phylib_coord *acc ) {
    if ( !pos || !vel || !acc ) {
        return NULL;
    }
    phylib_object *new_object = (phylib_object*) malloc( sizeof( phylib_object ) );
    if ( !new_object ) {
        return NULL;
    }
    new_object->type = PHYLIB_ROLLING_BALL;
    new_object->obj.rolling_ball.number = number;
    new_object->obj.rolling_ball.pos = *pos;
    new_object->obj.rolling_ball.vel = *vel;
    new_object->obj.rolling_ball.acc = *acc;
    return (phylib_object*) new_object;
}

/**
* Creates and returns a new phylib_hole object with values from the parameters.
* Returns NULL if memory could not be allocated or invalid arguments were
* entered.
*/         
phylib_object *phylib_new_hole( phylib_coord *pos ) {
    if ( !pos ) {
        return NULL;
    }
    phylib_object *new_object = (phylib_object*) malloc( sizeof( phylib_object ) );
    if ( !new_object ) {
        return NULL;
    }
    new_object->type = PHYLIB_HOLE;
    new_object->obj.hole.pos = *pos;
    return (phylib_object*) new_object;
}

/**
* Creates and returns a new phylib_hcushion object with values from the 
* parameters. Returns NULL if memory could not be allocated or invalid 
* arguments were entered.
*/
phylib_object *phylib_new_hcushion( double y ) {
    phylib_object *new_object = (phylib_object*) malloc( sizeof( phylib_object ) );
    if ( !new_object ) {
        return NULL;
    }
    new_object->type = PHYLIB_HCUSHION;
    new_object->obj.hcushion.y = y;
    return (phylib_object*) new_object;
}

/**
* Creates and returns a new phylib_vcushion object with values from the 
* parameters. Returns NULL if memory could not be allocated or invalid 
* arguments were entered.
*/
phylib_object *phylib_new_vcushion( double x ) {
    phylib_object *new_object = (phylib_object*) malloc( sizeof( phylib_object ) );
    if ( !new_object ) {
        return NULL;
    }
    new_object->type = PHYLIB_VCUSHION;
    new_object->obj.vcushion.x = x;
    return (phylib_object*) new_object;
}

/**
* Creates and returns a new phylib_table object with values from the 
* parameters. Returns NULL if memory could not be allocated or invalid 
* arguments were entered.
*/
phylib_table *phylib_new_table( void ) {
    phylib_table *new_table = (phylib_table*) malloc( sizeof( phylib_table ) );
    if ( !new_table) {
        return NULL;
    }
    new_table->time = 0.0;
    for ( int i = 0; i < PHYLIB_MAX_OBJECTS; i += 1 ) {
        new_table->object[i] = NULL;
    }
    phylib_add_object( new_table, phylib_new_hcushion( 0.0 ) );
    phylib_add_object( new_table, phylib_new_hcushion( PHYLIB_TABLE_LENGTH ) );
    phylib_add_object( new_table, phylib_new_vcushion( 0.0 ) );
    phylib_add_object( new_table, phylib_new_vcushion( PHYLIB_TABLE_WIDTH ) );
    phylib_coord new_coord = phylib_new_coord( 0.0, 0.0 );
    phylib_add_object( new_table, phylib_new_hole( &new_coord ) );
    new_coord = phylib_new_coord( 0.0, PHYLIB_TABLE_WIDTH );
    phylib_add_object( new_table, phylib_new_hole( &new_coord ) );
    new_coord = phylib_new_coord( 0.0, PHYLIB_TABLE_LENGTH );
    phylib_add_object( new_table, phylib_new_hole( &new_coord ) );
    new_coord = phylib_new_coord( PHYLIB_TABLE_WIDTH, 0.0 );
    phylib_add_object( new_table, phylib_new_hole( &new_coord ) );
    new_coord = phylib_new_coord( PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_WIDTH );
    phylib_add_object( new_table, phylib_new_hole( &new_coord ) );
    new_coord = phylib_new_coord( PHYLIB_TABLE_WIDTH
                                  , PHYLIB_TABLE_LENGTH);
    phylib_add_object( new_table, phylib_new_hole( &new_coord ) );
    for ( int index = 0; index < 10; index += 1 ) {
        if ( new_table->object[index] == NULL ) {
            phylib_free_table( new_table );
            return NULL;
        }
    }
    return (phylib_table*) new_table;
}

// Utility Functions

/**
* Creates a new phylib_object with the contents of the srcs object 
*/
void phylib_copy_object( phylib_object **dest, phylib_object **src ) {
    if (!dest) {
        return /*void*/;
    }
    if (!src || !(*src)) {
        *dest = NULL;
        return /*void*/;
    }
    *dest = (phylib_object*) malloc(sizeof(phylib_object));
    (*dest)->type = (*src)->type;
    (*dest)->obj = (*src)->obj;
}

/**
* Creates a new phylib_table with the same contents as the table paramater
*/
phylib_table *phylib_copy_table( phylib_table *table ) {
    if ( !table ) {
        return NULL;
    }
    phylib_table *table_copy = (phylib_table*) malloc(sizeof(phylib_table));
    if ( !table_copy ) {
        return NULL;
    }
    table_copy->time = table->time;
    for ( int i = 0; i < PHYLIB_MAX_OBJECTS; i++ ) {
        /*
        if (table_copy->object[i] != NULL) {
            table_copy->object[i] = NULL;
        }
        */
        phylib_copy_object( &(table_copy->object[i]), &(table->object[i]) );
    } 
    return (phylib_table*) table_copy;
}

/**
* adds the object to the first open position in the table object array
*/
void phylib_add_object(phylib_table *table, phylib_object *object) {
    if (!table) {
        return /*void*/;
    }
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (!(table->object[i])) {
            table->object[i] = object;
            return /*void*/;
        }
    }
}

/**
* Frees the memory allocated for a table object
*/
void phylib_free_table(phylib_table *table) {
    if (!table) {
        return /*void*/;
    }
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] != NULL) { // if not null
            free(table->object[i]);
        }
    }
    free(table);
}

/**
* Subtracts the corresponding coordinates of c2 from c1
*/
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2) {
    return phylib_new_coord((c1.x - c2.x), (c1.y - c2.y));
}

/**
* Calculates the length the input coordinate vector
*/                    
double phylib_length(phylib_coord c) {
    return sqrt((c.x * c.x) + (c.y * c.y));
}

/**
* Calculates the dot products of the input coordinates 
*/
double phylib_dot_product(phylib_coord a, phylib_coord b) {
    return ((a.x * b.x) + (a.y * b.y));
}

/**
* Calculates the distance between obj1 and obj2.
* obj1 must be a rolling ball
*/
double phylib_distance( phylib_object *obj1, phylib_object *obj2 ) {
    // obj1 must be a rolling ball
    if ( !obj1 || !obj2 ) {
        return (double) -1.0;
    }
    if ( obj1->type != PHYLIB_ROLLING_BALL ) {
        return (double) -1.0;
    }
    switch ( obj2->type ) {
        case PHYLIB_STILL_BALL: 
        {
            phylib_coord distance_vector = phylib_sub( obj1->obj.rolling_ball.pos
                                                     , obj2->obj.still_ball.pos );
            double distance = phylib_length( distance_vector );
            distance = distance - ( 2 * PHYLIB_BALL_RADIUS );
            return (double) distance;
        }
        case PHYLIB_ROLLING_BALL:
        {
            phylib_coord distance_vector = phylib_sub( obj1->obj.rolling_ball.pos
                                                     , obj2->obj.rolling_ball.pos );
            double distance = phylib_length( distance_vector );
            distance = distance - ( 2 * PHYLIB_BALL_RADIUS );
            return (double) distance;
        }
        case PHYLIB_HOLE:
        { 
            phylib_coord distance_vector = phylib_sub( obj1->obj.rolling_ball.pos
                                                     , obj2->obj.hole.pos );
            double distance = phylib_length( distance_vector );
            distance = distance - PHYLIB_HOLE_RADIUS;
            return (double) distance;
        }
        case PHYLIB_HCUSHION:
        {
            double distance = fabs( obj1->obj.rolling_ball.pos.y
                                  - obj2->obj.hcushion.y );
            distance = distance - PHYLIB_BALL_RADIUS;
            return (double) distance;
        }
        case PHYLIB_VCUSHION:
        {
            double distance = fabs( obj1->obj.rolling_ball.pos.x
                                  - obj2->obj.vcushion.x );
            distance = distance - PHYLIB_BALL_RADIUS;
            return (double) distance;
        }
        default:
            return (double) -1.0;
    }
}

// Physics Functions

/**
* Calculates the new position value given start position, velocity, and acceleration
*/
double phylib_update_position( double pos, double vel
                            , double acc, double time ) {
    double position = pos + ( vel * time ) 
        + ( ( 0.5 ) * acc * ( time * time ) );
    return (double) position;
}

/**
* Calculates the change in velocity given the acceleration
*/
double phylib_update_velocity( double vel, double acc, double time ) {
    double velocity = vel + (acc * time);
    return (double) velocity;
}

/**
* Updates new to have the values of old after it has rolled for a period of time.
*/
void phylib_roll( phylib_object *new, phylib_object *old, double time ) {
    if ( !new || !old ) {
        new = NULL;
        return /*void*/;
    }
    if ( new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL ) {
        return /*void*/;
    }
    new->obj.rolling_ball.pos.x = phylib_update_position( old->obj.rolling_ball.pos.x
                                                        , old->obj.rolling_ball.vel.x
                                                        , old->obj.rolling_ball.acc.x
                                                        , time );
    new->obj.rolling_ball.pos.y = phylib_update_position( old->obj.rolling_ball.pos.y
                                                        , old->obj.rolling_ball.vel.y
                                                        , old->obj.rolling_ball.acc.y
                                                        , time );
    new->obj.rolling_ball.vel.x = phylib_update_velocity( old->obj.rolling_ball.vel.x
                                                        , old->obj.rolling_ball.acc.x
                                                        , time );
    new->obj.rolling_ball.vel.y = phylib_update_velocity( old->obj.rolling_ball.vel.y
                                                        , old->obj.rolling_ball.acc.y
                                                        , time );
    if ( (new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x) < 0.0 ) {
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }                    
    if ( (new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y) < 0.0 ) {
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }
}

/**
* Checks if a phylib_rolling_ball is still and converts it to a phylib_still_ball.
* returns 1 if it turned object into a still_ball, 0 otherwise.
*/
unsigned char phylib_stopped( phylib_object *object ) {
    if ( !object ) {
        return (unsigned char) 0;
    }
    if ( object->type != PHYLIB_ROLLING_BALL ) {
        return (unsigned char) 0;
    }
    double speed = phylib_length( object->obj.rolling_ball.vel );
    if ( speed >= PHYLIB_VEL_EPSILON ) {
        return (unsigned char) 0;
    }
    object->type = PHYLIB_STILL_BALL;
    return (unsigned char) 1;
}

/**
* Handles the collisions between a rolling ball and other objects
*/
void phylib_bounce( phylib_object **a, phylib_object **b ) {
    if ( !a || !b || !(*a) || !(*b) ) {
        return /*void*/;
    }
    if ( (*a)->type != PHYLIB_ROLLING_BALL ) {
        return /*void*/;
    }
    phylib_rolling_ball *ball_a = (phylib_rolling_ball*) &( (*a)->obj );

    switch( (*b)->type ) {
        case PHYLIB_HCUSHION:
        {
            (*a)->obj.rolling_ball.acc.y = (*a)->obj.rolling_ball.acc.y * (-1.0);
            (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y * (-1.0);
            break;
        }
        case PHYLIB_VCUSHION:
        {
            (*a)->obj.rolling_ball.acc.x = (*a)->obj.rolling_ball.acc.x * (-1.0);
            (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x * (-1.0);
            break;
        }
        case PHYLIB_HOLE:
        {
            free( *a );
            *a = NULL;
            break;
        }
        case PHYLIB_STILL_BALL:
        {
            phylib_coord vel = phylib_new_coord( 0.0, 0.0 );
            phylib_coord acc = phylib_new_coord( 0.0, 0.0 );
            phylib_object *ball_b = phylib_new_rolling_ball( (*b)->obj.still_ball.number
                                                           , &((*b)->obj.still_ball.pos)
                                                           , &vel, &acc);
            free( *b );
            *b = ball_b;
        }
        case PHYLIB_ROLLING_BALL:
        {
            phylib_rolling_ball *ball_b = (phylib_rolling_ball*) &( (*b)->obj );
            // get relative position vector
            phylib_coord r_ab = phylib_sub( ball_a->pos, ball_b->pos );
            // get relative velocity vector
            phylib_coord v_rel = phylib_sub( ball_a->vel, ball_b->vel );
            // get normalized relative position vector
            double r_ab_length = phylib_length( r_ab );
            phylib_coord n = r_ab;
            n.x = n.x / r_ab_length;
            n.y = n.y / r_ab_length;
            // calculate relative velocity
            double v_rel_n = phylib_dot_product( v_rel, n );
            //
            ball_a->vel.x = ball_a->vel.x - ( v_rel_n * n.x );
            ball_a->vel.y = ball_a->vel.y - ( v_rel_n * n.y );
            ball_b->vel.x = ball_b->vel.x + ( v_rel_n * n.x );
            ball_b->vel.y = ball_b->vel.y + ( v_rel_n * n.y );

            if ( phylib_length( ball_a->vel ) > PHYLIB_VEL_EPSILON ) {
                ball_a->acc.x = (((ball_a->vel.x * (-1.0)) / phylib_length( ball_a->vel )) * PHYLIB_DRAG);
                ball_a->acc.y = (((ball_a->vel.y * (-1.0)) / phylib_length( ball_a->vel )) * PHYLIB_DRAG);
            } else {
                ball_a->acc.x = 0.0;
                ball_a->acc.y = 0.0;
            }
            if ( phylib_length( ball_b->vel ) > PHYLIB_VEL_EPSILON ) {
                ball_b->acc.x = (((ball_b->vel.x * (-1.0)) / phylib_length( ball_b->vel )) * PHYLIB_DRAG);
                ball_b->acc.y = (((ball_b->vel.y * (-1.0)) / phylib_length( ball_b->vel )) * PHYLIB_DRAG);
            }
            break;
        }
        default:
        {
            break;
        }
    }
}

/**
* 
*/
unsigned char phylib_rolling( phylib_table *t ) {
    if (!t) {
        return (unsigned char) 0;
    }
    unsigned char num_rolling_balls = 0;
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (!(t->object[i])) {
            continue;
        }
        if (t->object[i]->type == PHYLIB_ROLLING_BALL) {
            num_rolling_balls++;
        }
    }
    return (unsigned char) num_rolling_balls;
}

phylib_table *phylib_segment(phylib_table *table) {
    if (!table || phylib_rolling(table) == 0) {
        return NULL;
    }
    phylib_table *table_copy = phylib_copy_table(table);
    table_copy->time = table_copy->time + PHYLIB_SIM_RATE;
    double time = PHYLIB_SIM_RATE;
    while (time < PHYLIB_MAX_TIME) {
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            if (!table_copy->object[i] || table_copy->object[i]->type != PHYLIB_ROLLING_BALL) {
                continue;
            }

            phylib_object *new_ball;
            phylib_copy_object( &new_ball, &(table_copy->object[i]));
            phylib_roll(new_ball, table_copy->object[i], PHYLIB_SIM_RATE);
            free(table_copy->object[i]);
            table_copy->object[i] = new_ball;
        }
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            if (!table_copy->object[i] || table_copy->object[i]->type != PHYLIB_ROLLING_BALL) {
                continue;
            }
            if (phylib_stopped(table_copy->object[i])) {
                table_copy->time += time;
                return table_copy;
            }
            for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
                if (j == i || !table_copy->object[j]) {
                    continue;
                }
                if (phylib_distance(table_copy->object[i], table_copy->object[j]) <= 0.0) {
                    phylib_bounce(&(table_copy->object[i]), &(table_copy->object[j]));
                    table_copy->time += time;
                    return table_copy;
                }
            }
        }
        time += PHYLIB_SIM_RATE;
    }
    table_copy->time += time;
    return table_copy;
} 

char *phylib_object_string( phylib_object *object ) {
    static char string[80];
    if (object == NULL) {
    snprintf( string, 80, "NULL;" );
        return string;
    }
    switch (object->type) {
        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
            "STILL_BALL (%d,%6.1lf,%6.1lf)",
            object->obj.still_ball.number,
            object->obj.still_ball.pos.x,
            object->obj.still_ball.pos.y );
            break;
        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,
            "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
            object->obj.rolling_ball.number,
            object->obj.rolling_ball.pos.x,
            object->obj.rolling_ball.pos.y,
            object->obj.rolling_ball.vel.x,
            object->obj.rolling_ball.vel.y,
            object->obj.rolling_ball.acc.x,
            object->obj.rolling_ball.acc.y );
            break;
        case PHYLIB_HOLE:
            snprintf( string, 80,
            "HOLE (%6.1lf,%6.1lf)",
            object->obj.hole.pos.x,
            object->obj.hole.pos.y );
            break;
        case PHYLIB_HCUSHION:
            snprintf( string, 80,
            "HCUSHION (%6.1lf)",
            object->obj.hcushion.y );
            break;
        case PHYLIB_VCUSHION:
            snprintf( string, 80,
            "VCUSHION (%6.1lf)",
            object->obj.vcushion.x );
            break;
    }
return string;
}
