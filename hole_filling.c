#include <stdio.h>
#include <stdlib.h>

const int DX[] = {1, 0, -1, 0};
const int DY[] = {0, 1, 0, -1};

typedef struct{
	int s;
	int *a;
	int capacity;
}vector;

typedef struct{
	int s;
	int a[2];
} two_element_set;

typedef struct{
	int nbBgRegions; // number of background regions
	int *neighbor;
	int *visited;
}answer;


void vector_init(vector *v, int init_size){
	v->s = 0;
	v->capacity = init_size;
	v->a = (int *)malloc(sizeof(int) * init_size);
}

void vector_resize(vector *v, int size){
	int *p = v->a;
	v->a = (int *)malloc(sizeof(int) * size);
	v->capacity = size;
	for(int i = 0; i < v->s; i++) v->a[i] = p[i];
	free(p);
}

void vector_pushback(vector *v, int value){
	if(v->s >= v->capacity)
		vector_resize(v, 2 * v->capacity);
	v->a[v->s++] = value;
}

void vector_free(vector *v){
	free(v->a);
	v->s = v->capacity = 0;
}

void set_init(two_element_set *ts){
	ts->s = 0;
}

void set_insert(two_element_set *ts, int value){
	if(ts->s == 0)
		ts->a[ts->s++] = value;
	else if(ts->s == 1){
		if(ts->a[0] != value)
			ts->a[ts->s++] = value;
	}
}

int in_range(int i, int j, int h, int w){
    // test 0 <= i < h && 0 <=j < w
	return 0 <= i && i < h && 0 <= j && j < w;
}

/*
 *   Visit the mask from position `pos` and mark every visited position with
 * integer `count`. `wq` is a pre-allocated buffer used as working memory.
 *
 * Return
 *   -2 indicates multiple neighbors or an integer greater than -2 indicates
 * the only one neighbor.
 */
int visit_from(int *mask, int *wq, int *visited, int h, int w, int pos, int count){
	two_element_set ts;
	set_init(&ts);

	int head = 0, tail = 0;
	wq[tail++] = pos;
	visited[pos] = count;
	int cur_pos = -1, pi = -1, pj = -1, ni = -1, nj = -1, next_pos = -1;
	while(head != tail){
		cur_pos = wq[head++];
		pi = cur_pos / w;
		pj = cur_pos % w;
		for(int k = 0; k < 4; k++){
			ni = pi + DX[k];
			nj = pj + DY[k];
			next_pos = ni * w + nj;
			if(in_range(ni, nj, h, w)){
				if(mask[next_pos] == 0 && visited[next_pos] == -1){
					wq[tail++] = next_pos;
					visited[next_pos] = count;
				}
				if(mask[next_pos]){
					set_insert(&ts, mask[next_pos]);
				}
			}else{
				set_insert(&ts, -1);
			}
		}
	}
	return ts.s == 1 ? ts.a[0] : -2;
}

answer *count_neighbor(int *mask, int h, int w){
	vector neighbor;
	vector_init(&neighbor, 10);
	int count = 0;
	int *visited = (int *)malloc(sizeof(int) * h * w);
	for(int i = 0; i < h * w; i++) visited[i] = -1;

    // pre-allocate working memory for efficiency
	int *wq = (int *)malloc(sizeof(int) * h * w);

	for(int pos = 0; pos < h * w; pos++){
		if(visited[pos] == -1 && mask[pos] == 0){
			int nbor = visit_from(mask, wq, visited, h, w, pos, count);
			vector_pushback(&neighbor, nbor);
			count++;
		}
	}
	free(wq);

	answer *a = (answer *)malloc(sizeof(answer));
	a->nbBgRegions = neighbor.s;
	a->neighbor = neighbor.a;
	a->visited = visited;

	return a;
}

void answer_free(answer *p){
	free(p->neighbor);
	free(p->visited);
}
