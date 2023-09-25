import numpy as np

#1m-9m,1p-9p,1s-9s,tnsphhc
test1=np.array([0,1,1,1,0,0,0,0,2, 0,0,0,0,1,1,0,0,1, 0,0,0,3,0,0,2,0,1, 0,0,0,0,0,0,0])#2m 3m 4m 9m 9m 5p 6p 9p 4s 4s 4s 7s 7s 9s
#test1=np.array([0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0])

souhai=np.sum(test1) #総牌(麻雀=14)

#yakul=np.array([0,1,2])
#yakux=np.array([[0,0,0,1,2],[1,0,0,0,1],[0,1,0,1,0]]) 

yakux=np.zeros(1,dtype=int) #【上から必要牌数が多い順に並べておく】

def normal_mahjong():
    re=np.zeros((89,34),dtype=int)
    for i in range(3): #順子
        for j in range(7):
            re[i*7+j][i*9+j]=1
            re[i*7+j][i*9+j+1]=1
            re[i*7+j][i*9+j+2]=1
    for i in range(34):
        re[i+21][i]=3
        re[i+55][i]=2
    
    return re

yakux=normal_mahjong()
#print(yakux)

yakusumx=np.sum(yakux,axis=1)
shurui=yakux.shape[1] #牌の種類数(四人麻雀=34)
yakusuu=yakux.shape[0] #役の総数(四人麻雀=順子21+刻子34+対子34=89)

rkl=[0 for i in range(yakusuu)]
arr=np.arange(yakusuu)

h=souhai+1

def retsu_add1(mx,b):#特定の列全要素に+1
    zo0=np.zeros(mx.shape[1],dtype=int)
    zo0[b]+=1
    zo1=np.tile(zo0,(mx.shape[0],1))
    return mx+zo1

def unit_pattern_start(fl):
    if np.sum(fl)>0:
        fl2=np.tile(fl,(yakusuu,1))
        rex=fl2-yakux
        minusx=np.where(rex>0,0,-rex)
        hx=np.sum(minusx,axis=1)#ユニットを引いた結果ごとのh
        omomix=hx*10*yakusuu+arr
        turnx=np.argsort(omomix)
        global rkl
        for i in range(yakusuu):
            rkl[turnx[i]]=i
    return unit_pattern(fl,souhai+1,0)

def unit_pattern(fl,h0,u0): #fl:残ってる牌 h0:hのノルマ u0:ここまで確かめた(大きい方から) return:h,[できる役,捨て牌&欲しい牌]のリスト
    nowh=h0
    zan=np.sum(fl)
    #print("->",zan)
    if zan==0:
        zettai=np.abs(fl)
        return np.sum(zettai)//2,np.zeros((1,yakusuu),dtype=int),np.tile(fl,(1,1))
    elif zan>1:
        fl2=np.tile(fl,(yakusuu,1))
        rex=fl2-yakux
        minusx=np.where(rex>0,0,-rex)
        hx=np.sum(minusx,axis=1)#ユニットを引いた結果ごとのh
        omomix=hx*10*yakusuu+arr
        #print(hx)
        turnx=np.argsort(omomix)
        #print(turnx)
        #return 0
        reyakux=np.array([-1])#できる役のreリスト
        rerex=np.array([-1])#捨て牌&欲しい牌のreリスト
        for i in range(yakusuu):
            t=turnx[i]
            #print("-->  ",zan,t)
            if nowh<hx[t]:
                break
            if rkl[t]<u0:#被り処理
                continue
            if zan<yakusumx[t] or zan==yakusumx[t]+1:#牌を使い過ぎるor1だけ余る
                continue
            nowp=rex[t]
            h1,yakux1,rex1=unit_pattern(nowp,nowh,rkl[t])
            #print("<-       ",h1)
            if np.all(yakux1==-1):
                continue
            if h1<nowh:
                nowh=h1
                reyakux=yakux1
                rerex=rex1
                reyakux=retsu_add1(reyakux,t)
            elif h1==nowh:
                if np.all(reyakux==-1):
                    reyakux=yakux1
                    rerex=rex1
                    zo0=np.zeros(yakusuu,dtype=int)
                    zo0[t]+=1
                    zo1=np.tile(zo0,(reyakux.shape[0],1))
                    reyakux+=zo1
                else:
                    yakux1=retsu_add1(yakux1,t)
                    reyakux=np.vstack((reyakux,yakux1))
                    rerex=np.vstack((rerex,rex1))
        if np.all(reyakux==-1):
            return souhai+1,np.array([-1]),np.array([-1])
        else:
            refusion=np.hstack((reyakux,rerex))
            refusion2=np.unique(refusion,axis=0)
            reyakux,rerex=np.split(refusion2,[yakusuu],1)
            return nowh,reyakux,rerex
    else:
        return souhai+1,np.array([-1]),np.array([-1])


h_r,y_r,p_r=unit_pattern_start(test1)
for i in range(y_r.shape[0]):
    print("役 ",end="")
    for j in range(y_r.shape[1]):
        if y_r[i][j]>0:
            for k in range(y_r[i][j]):
                print(j,end=" ")
    print("欲 ",end="")
    for j in range(p_r.shape[1]):
        if p_r[i][j]<0:
            for k in range(-p_r[i][j]):
                print(j,end=" ")
    print("捨 ",end="")
    for j in range(p_r.shape[1]):
        if p_r[i][j]>0:
            for k in range(p_r[i][j]):
                print(j,end=" ")
    print("")
