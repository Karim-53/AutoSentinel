#include <bits/stdc++.h>
using namespace std;
#include <iostream>
#include <windows.h>

const WORD colors[] =
		{
		0x1A, 0x2B, 0x3C, 0x4D, 0x5E, 0x6F,
		0xA1, 0xB2, 0xC3, 0xD4, 0xE5, 0xF6
		};

	HANDLE hstdin  = GetStdHandle( STD_INPUT_HANDLE  );
	HANDLE hstdout = GetStdHandle( STD_OUTPUT_HANDLE );
	WORD   index   = 0;

	// Remember how things were when we started
	CONSOLE_SCREEN_BUFFER_INFO csbi;

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
int next_pos;
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
    //DONE: tant que y'a bfs �a marchera pas

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
            if (matrix[i][j]==100){//SetConsoleTextAttribute( hstdout, csbi.wAttributes );
                cout<<"      ";
            }
            else{

                if (matrix[i][j]==116) SetConsoleTextAttribute( hstdout, colors[ 11 ] );
                if (matrix[i][j]==123) SetConsoleTextAttribute( hstdout, colors[ 5 ] );
                if (matrix[i][j]==116) SetConsoleTextAttribute( hstdout, colors[ 3 ] );
                if (matrix[i][j]==999) SetConsoleTextAttribute( hstdout, colors[ 11 ] );
                cout<<matrix[i][j]<<"   ";//printf("%d   ", );
                // Keep users happy
                SetConsoleTextAttribute( hstdout, colors[ 0 ] );
//                SetConsoleTextAttribute( hstdout, csbi.wAttributes );
}

        cout<<'\n';//printf("\n");
    }
        printf("______\n\n");
}


ull dist[nax];
int BT[nax];
double dijkstra(int src, int snk){//TODO: passer � min coast max flow (pas sur que c'est mieux min risque max speed)
    priority_queue<pair<ull,int>,vector<pair<ull,int>>, greater<pair<ull,int>>> q;
    //priority_queue< pair<ull,int> > q;
    q.push({Dj_val_min,src});
    memset(dist, Dyjkestra_infinite, nax*(sizeof dist[0]));//initialis� � l'inf
    memset(BT, Dyjkestra_infinite, nax*(sizeof BT[0]));//initialis� � l'inf
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


void color_map(int u)
{
int x = u/n;
int y =  u%n;
_map[x][y] = 999;
//cout<<u<<"  "<<  visited[x][y] <<endl;

if ( BT[u] == 0 || BT[BT[u]] == 0 ){
    next_pos = u;
    return ;
}
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


        if (snc_x<10){
            SetWall(20, 3);
        }
        if (snc_x<9){
            SetWall(19, 4);
        }
        if (snc_x<8){
            SetWall(18, 5);
        }
        if (snc_x<7){
            for(int j = 20;j>9;j--)
                SetWall(j, 5);
        }



   // print(_map);

    //load zones inconu
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            _map[i][j] += INCONU;
   // print(_map);

    _map[src_x][src_y] = 123;//start

    //cible fixe pour l'instant
    //snc_x = 5;
    //snc_y = 5;
    if ( dijkstra(src_x*n+src_y, snc_x*n+snc_y) == -1 ){
    cout<< "pas de chemin optimal\n";
    return 1;
    }

    color_map(snc_x*n+snc_y);

  print(_map);

//vecteur deplacement:
int nxt_x = next_pos/n;
int nxt_y = next_pos%n;
int vec_dep_x = nxt_x - src_x;
int vec_dep_y = nxt_y - src_y;
cout<<"vecteur deplacement: "<<vec_dep_x<<"      "<<vec_dep_y<<endl;
//DONE: faire bouger le pt src d'un pas � chaque iteration
src_x+=vec_dep_x;
src_y+=vec_dep_y;
    return 0;

}
#include <iostream>
#include <windows.h>
int main()
{
while (1)
	{
		SetConsoleTextAttribute( hstdout, colors[ index ] );
		std::cout << "\t\t\t\t Hello World "<<index<<" \t\t\t\t" << std::endl;
		if (++index > sizeof(colors)/sizeof(colors[0]))
			break;
	}
       /*
        char c;
        cin>>c;
        */
    //TODO si la snc  == MUR -> trouver les pts les plus proches

    //Soit le drone � la pos
     src_x = 22;
     src_y = 22;

    snc_y = 5;
    for( snc_x = 20;snc_x>5;snc_x--)
    {
    _main();

        char c;
        cin>>c;

    }
    return 0;
}
//TODO: zones inconu + zones explor�e
//TODO: implementer cette exemple dans le simulateur
//TODO: extraire le vecteur deplacement (vec AB: src->next step)
//TODO: choisir entre les 2 trajet: moin de risque ou plus directe, var priorit�
//TODO: considerer la vitesse de l'air
//TODO: chnager l'output: vecteur deplacement -> vacteur vitesse
 //TODO: passer vers un model 3d
/*  TODO: recalc le rapport cout risque - cout distance
    taw = 102*A+2*1.41*B
    sinon = 104*A+2*1.00*B
*/
