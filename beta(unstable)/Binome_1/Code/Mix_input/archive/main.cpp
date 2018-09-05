#include <bits/stdc++.h>
using namespace std;



//param user
int const n = 28;//taille map

// param coder
#define MUR     4
#define INCONU  100
#define CONU    0

#define ull                 unsigned long long
#define ll                  long long
#define Dyjkestra_infinite 78400LL
#define Dj_val_min  0
#define nax         n*n
#define null -1
int src_x;
int src_y;
    int snc_x;
    int snc_y;
int dx[] = {0,1,1,1,0,-1,-1,-1};
int dy[] = {1,1,0,-1,-1,-1,0,1};
int _map[n][n];
vector<vector<int> > visited;
#define rep(i,n) for(auto i = 0; i<n ; i++)


void SetWall(int x, int y)
{
    //_map[x][y] = max(_map[x][y],16);
    //DONE: tant que y'a bfs ça marchera pas

// defini les zones interdites et tt ce qui proche de ces zones
    for(int i=x-2;i<=x+2;++i)
        for(int j=y-2;j<=y+2;++j)
            _map[i][j] = max(_map[i][j],1<<(MUR-(abs(i-x)+abs(j-y)) ) );

}


void print(int matrix[n][n])
{
    int i, j;
    for (i = 0; i < n; ++i)
    {
        for (j = 0; j < n; ++j)
            if (matrix[i][j]==100)
                cout<<"      ";
            else
                printf("%d   ", matrix[i][j]);


        printf("\n");
    }
        printf("\n\n");
}


ull dist[nax];
int BT[nax];
double dijkstra(int src, int snk){//min risque max speed
    priority_queue<pair<ull,int>,vector<pair<ull,int>>, greater<pair<ull,int>>> q;
    //priority_queue< pair<ull,int> > q;
    q.push({Dj_val_min,src});
    memset(dist, Dyjkestra_infinite, nax*(sizeof dist[0]));//initialisé à l'inf
    memset(BT, Dyjkestra_infinite, nax*(sizeof BT[0]));//initialisé à l'inf
                dist[src]=0;
                BT[src]=0;//back track
    while(q.size()){
        double d=q.top().first;//distance
        int cur=q.top().second;//cur pos
      //  cerr<<cur<<endl;
        q.pop();
        if(d>dist[cur])
            continue;
        if(snk==cur)
            return d;

        int x = cur/n;
        int y = cur%n;
//cerr<<x<<" "<<y<<endl;
        for (auto i=0;i<8;i++)
        {
            int xx = x+dx[i];
            int yy = y+dy[i];
            int t = xx*n + yy;
            if (!(xx>0 && yy>0 && xx<n && yy<n)) continue;

            ll dd= (_map[xx][yy]-100)*1000 +d+(dx[i]*dy[i]==0 ? 100 : 141) ;
           // cout<<t<<"  "<<dist[t]<<" "<<dd<<endl<<endl;
            if(dist[t]>dd){
                dist[t]=dd;
                BT[t]=cur;//back track
                q.push({dd,t});
            }
        }
    }
    return -1;
}

vector<vector<int> > bfs(int src_x, int src_y)
{
    //  mark all distance with -1
    vector<vector<int> > visited(n,vector<int>(n,-1) );
    visited[src_x][src_y]=0;
    queue<int> q;
    q.push(src_x*1000+src_y);

    while (!q.empty())
    {
        int t = q.front();       q.pop();
        int x = t/1000;
        int y = t%1000;
        //  loop for all adjacent nodes
        for (auto i=0;i<8;i++)
        {
            int xx = x+dx[i];
            int yy = y+dy[i];
            if (!(xx>0 && yy>0 && xx<n && yy<n)) continue;
            // push node into queue only if
            // it is not visited already
            if (visited[xx][yy]==-1)
            {
               visited[xx][yy]= x*1000+y;
                if ( _map[xx][yy] != ((1<<MUR) + INCONU) ){
                        q.push(xx*1000+yy);
                    if (xx==snc_x && yy==snc_y) return visited;

                }
            }
        }
    }
return visited; // on n'a pas trouvé de chemin
}

void color_map(int u)
{
int x = u/1000;
int y =  u%1000;
_map[x][y] = 999;
//cout<<u<<"  "<<  visited[x][y] <<endl;

if ( BT[u] == 0 ) return ;

color_map(BT[u]);
}

int _main()
{
    rep(i,n) rep(j,n) _map[i][j] = 0;
    //load zones interdites
    for(int j = 15 ; j<20;j++)
        SetWall(20, j);
    for(int j = 5 ; j<12;j++)
        SetWall(10, j);
   // print(_map);

    //load zones inconu
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            _map[i][j] += INCONU;
   // print(_map);

    //Soit le drone à la pos
     src_x = 22;
     src_y = 22;

    //cible fixe pour l'instant
    //snc_x = 5;
    //snc_y = 5;
    if ( dijkstra(src_x*n+src_y, snc_x*n+snc_y) == -1 ){
    cout<< "pas de chemin optimal\n";
    return 1;
    }

    color_map(snc_x*n+snc_y);

  print(_map);





    return 0;

}
int main()
{
    //TODO si la snc  == MUR -> trouver les pts les plus proches

    snc_y = 5;
for( snc_x = 20;snc_x>5;snc_x--)
     {
_main();

    char c;
     cin>>c;
}
return 0;
}
//TODO: faire bouger le pt src d'un pas à chaque iteration
//TODO: zones inconu + zones explorée
//TODO implementer cette exemple dans le simulateur
