import java.nio.Buffer;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class hashcode{
    public ArrayList<Photo> data;
    public ArrayList<Score> scores = new ArrayList<Score>();

    private int min(int commonTag, int missingTag1, int missingTag2) {
        if(commonTag <= missingTag1 && commonTag <= missingTag2){
            return commonTag;
        }else if(missingTag1 <= commonTag && missingTag1 <= missingTag2){
            return missingTag1;
        }else{
            return missingTag2;
        }
    }

    public void printAllInfo(){
        for(Photo photo : this.data){
            System.out.println("Name: " + photo.getName());
            System.out.println("Type: " + photo.getType());
            System.out.print("Tags: ");
            for(String tag : photo.getTags()){
                System.out.print(tag + " ");
            }
            System.out.println();
            System.out.println("Used: " + photo.getUsed());
            System.out.println();
        }
    }

    public hashcode(String pathToFile){

        readFile rf = new readFile();
        String filePath = pathToFile;
        this.data = rf.read(filePath);
        System.out.println("Parsed File Data: " + filePath + "\n");

    }

    public Integer scoring(Photo photo1, Photo photo2){
        int commonTag = commonTag(photo1, photo2);
        if(commonTag == 0){ return 0;}
        int missingTag1 = missingTag(photo1, photo2);
        if(missingTag1 == 0){return 0;}
        int missingTag2 = missingTag(photo2, photo1);
        int score = min(commonTag, missingTag1, missingTag2);
        if(score != 0){
            //scores.add(new Score(photo1, photo2, score));  
        }
        return score;
    }

    public int commonTag(Photo photo1, Photo photo2){
        Set<String> tags1 = new HashSet<>(List.of(photo1.getTags()));
        Set<String> tags2 = new HashSet<>(List.of(photo2.getTags()));
        
        tags1.retainAll(tags2);
        return tags1.size();
    }
        
    public int missingTag(Photo photo1, Photo photo2){
        Set<String> tags1 = new HashSet<>(List.of(photo1.getTags()));
        Set<String> tags2 = new HashSet<>(List.of(photo2.getTags()));

        tags1.removeAll(tags2);
        return tags1.size();
    }

    public void combinedPhoto(){
        for(int i = 0; i < this.data.size(); i++){
            if(this.data.get(i).getType().equals("V")){
                for(int j = i+1; j < this.data.size(); j++){
                    if(i != j && this.data.get(j).getType().equals("V")){
                        String[] tag = tagCombined(this.data.get(i), this.data.get(j));
                        Photo PhotoCombined = new Photo("Photo"+ i + " Photo"+j, "C", tag); 
                        this.data.add(PhotoCombined);              
                    }
                }
            }
        }
    }

    public String[] tagCombined(Photo photo1, Photo photo2){
        String[] tags1 = photo1.getTags();
        String[] tags2 = photo2.getTags();
        String[] tmp = new String[tags1.length + tags2.length];
        int size = tags1.length;
        for(int i = 0; i < tags1.length; i++){
            tmp[i] = tags1[i];
        }
        for(int i = 0; i < tags2.length; i++){
            boolean add = true;
            for(int j = 0; j < tags1.length; j++){
                if(tags2[i].equals(tags1[j])){
                    add = false;
                    break;
                }
            }
            if(add){
                tmp[size] = tags2[i];
                size++;
            }
        }

        String[] combined = new String[size];
        for(int i = 0; i < size; i++){
            combined[i] = tmp[i];
        }

        return combined;


    }
 
    public boolean isContained(Photo photo1, Photo photo2){
        Set<String> names1 = new HashSet<>(List.of(photo1.getName().split(" ")));
        Set<String> names2 = new HashSet<>(List.of(photo2.getName().split(" ")));
        
        names1.retainAll(names2);
        return !names1.isEmpty();
    }

    public void createSlideShow(){
        int random = (int) (Math.random() * this.data.size());
        Photo photo = this.data.get(random);
        setUsedPhoto(photo);
        maxScore(photo);
        setUsedPhoto(scores.get(scores.size()-1).getPhoto2());
        loopScore();

        readFile rf = new readFile();
        rf.writeFile(scores);

    }

    public void loopScore(){
        boolean isNull = false;

        while(!isNull){
            Photo photo = scores.get(scores.size()-1).getPhoto2();
            if(photo.getType().equals("C")){
                isNull = maxScoreCombined(photo);
            }
            else{isNull = maxScore(photo);}
                
            setUsedPhoto(photo);
        }

        System.out.println("Size of the scores: " + scores.size() + "\n");
        int total = 0;
        for(Score r: this.scores){
            total += r.getScore();
        }
        System.out.println("Total Score: " + total);

        
    }

    public boolean maxScore(Photo photo){
        int max = 0;
        Photo nextPhoto = null;
        for(Photo p: this.data){
            if(!p.getUsed() && !photo.getName().contains(p.getName())){
                int score = scoring(photo, p);
                if(nextPhoto == null){
                    nextPhoto = p;
                    max = score;
                }
                else if(score > max){
                    max = score;
                    nextPhoto = p;
                }
            }
        }
        if(nextPhoto != null){
            scores.add(new Score(photo, nextPhoto, max));
            return false;
        }
        return true;

    }

    public boolean maxScoreCombined(Photo photo){
        int max = 0;
        String[] names = photo.getName().split(" ");
        Photo nextPhoto = null;
        for(Photo p: this.data){
            if(!p.getUsed() && (!p.getName().contains(names[0]) && !p.getName().contains(names[1]))){
                int score = scoring(photo, p);
                if(nextPhoto == null){
                    nextPhoto = p;
                    max = score;
                }
                else if(score > max){
                    max = score;
                    nextPhoto = p;
                }
            }
        }
        if(nextPhoto != null){
            scores.add(new Score(photo, nextPhoto, max));
            return false;
        }
        return true;

    }

    public void setUsedPhoto(Photo photo){
        if(photo.getType().equals("C")){
            String[] names = photo.getName().split(" ");
            for(Photo p : this.data){
                if(p.getName().contains(names[0]) || p.getName().contains(names[1])){
                    p.setUsed(true);
                }
            }
        }
        else{
            for(Photo p : this.data){
                if(p.getName().contains(photo.getName())){
                    p.setUsed(true);
                }
            }
        }
    }

    public static void main(String[] args) {
        // if(args.length == 0){
        //     System.out.println("Please provide the file path");
        //     return;
        // }

        // String filePath = args[0];

        //hashcode m = new hashcode("a_example.txt");
        //hashcode m = new hashcode("c_memorable_moments.txt");
        //hashcode m = new hashcode("c_reduce_set.txt");
        hashcode m = new hashcode("b_lovely_landscapes.txt");
        m.combinedPhoto();

        System.out.println("Size of the dataSet: " + m.data.size());

        m.createSlideShow();
        
    }

}