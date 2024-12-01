import java.nio.Buffer;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class hashcode{
    public ArrayList<Photo> data;
    public ArrayList<Score> scores = new ArrayList<Score>();
    public ArrayList<Score> result = new ArrayList<Score>();

    private int max(int length, int length2) {
        if(length > length2){
            return length;
        }else{
            return length2;
        }
    }

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
            scores.add(new Score(photo1, photo2, score));  
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
        //sortScores();
        result.add(scores.get(0));
        scores.remove(0);
        setUsedPhoto(result.get(0).getPhoto1());
        setUsedPhoto(result.get(0).getPhoto2());

        loopScore();

        System.out.println("Size: " + result.size());
        int score = 0;
        for(Score s : result){
            score += s.getScore();
        }

        System.out.println("Score: " + score);

        readFile rf = new readFile();
        rf.writeFile(result);

    }

    public void loopScore(){
        boolean isZero = false;
        int[] max = new int[2];
        while(!scores.isEmpty() && !isZero)
        {
            max = maxScore(result.get(result.size()-1).getPhoto1());
            if(max[0] == 0){
                isZero = true;
            }else{
                result.add(scores.get(max[1]));
                scores.remove(max[1]);
                setUsedPhoto(result.get(result.size()-1).getPhoto1());
                setUsedPhoto(result.get(result.size()-1).getPhoto2());
            }
        }
        
    }

    public int[] maxScore(Photo photo){
        int max = 0;
        int index = 0;
        for(Score score : scores){
            if(
                (score.getPhoto1().getName().contains(photo.getName()) && !score.getPhoto2().getUsed()) ||
                (score.getPhoto2().getName().contains(photo.getName()) && !score.getPhoto1().getUsed())
            ){
                if(score.getScore() > max){
                    max = score.getScore();
                    index = scores.indexOf(score);
                }
            }
        }
        int[] result = new int[2];
        result[0] = max;
        result[1] = index;
        return result;
    }

    public void sortScores(){
        scores.sort((score1, score2) -> score2.getScore() - score1.getScore());
    }

    public void setUsedPhoto(Photo photo){
        for(Photo p : this.data){
            if(p.getName().contains(photo.getName())){
                p.setUsed(true);
            }
        }
    }

    public static void main(String[] args) {
        // if(args.length == 0){
        //     System.out.println("Please provide the file path");
        //     return;
        // }

        // String filePath = args[0];

        hashcode m = new hashcode("a_example.txt");
        m.combinedPhoto();

        for (int i = 0; i < m.data.size(); i++) {
            for (int j = i + 1; j < m.data.size(); j++) {
                if (!m.isContained(m.data.get(i), m.data.get(j))) {
                    m.scoring(m.data.get(i), m.data.get(j));
                }
            }
        }

        m.createSlideShow();
        
    }

}