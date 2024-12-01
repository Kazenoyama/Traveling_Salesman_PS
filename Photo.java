public class Photo {

    public String name;
    public String type;
    public boolean used;
    public String[] tags;
    public boolean combined;


    public Photo(String name, String type, String[] tags){
        this.name = name;
        this.type = type;
        this.tags = tags;
        this.used = false;
        this.combined = false;
    }
    
    public String getName(){
        return this.name;
    }

    public String getType(){
        return this.type;
    }

    public String[] getTags(){
        return this.tags;
    }

    public boolean getUsed(){
        return this.used;
    }

    public void setUsed(boolean used){
        this.used = used;
    }

    public boolean getCombined(){
        return this.combined;
    }

    public void setCombined(boolean combined){
        this.combined = combined;
    }
    
}
