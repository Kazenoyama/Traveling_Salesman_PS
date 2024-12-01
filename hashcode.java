import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class hashcode{
    public ArrayList<Photo> data;

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

    public hashcode(String pathToFile){

        readFile rf = new readFile();
        String filePath = pathToFile;
        this.data = rf.read(filePath);
        System.out.println("Parsed File Data: " + filePath + "\n");

    }

    public Integer scoring(Photo photo1, Photo photo2){
        int commonTag = commonTag(photo1, photo2);
        int missingTag1 = missingTag(photo1, photo2);
        int missingTag2 = missingTag(photo2, photo1);

        // System.out.println(photo1.getName() + " / " + photo2.getName());
        // System.out.println("Common tags: " + commonTag);
        // System.out.println("Missing tags 1: " + missingTag1);
        // System.out.println("Missing tags 2: " + missingTag2);

        int score = min(commonTag, missingTag1, missingTag2);

        // System.out.println("Score: " + score);



        return score;
    }

    public int commonTag(Photo photo1, Photo photo2){
        Set<String> tags1 = new HashSet<>(List.of(photo1.getTags()));
        Set<String> tags2 = new HashSet<>(List.of(photo2.getTags()));
        
        tags1.retainAll(tags2); // Finds common elements
        return tags1.size();

        // String tags1[] = photo1.getTags();
        // String tags2[] = photo2.getTags();
        // int common = 0;

        // String[] commonTag = new String[max(tags1.length, tags2.length)];
        // for(String tag1 : tags1){
        //     for(String tag2 : tags2){
        //         if(tag1.equals(tag2)){
        //             commonTag[common] = tag1;
        //             common++;
        //         }
        //     }
        // }

        // return common;
    }
        
    public int missingTag(Photo photo1, Photo photo2){
        Set<String> tags1 = new HashSet<>(List.of(photo1.getTags()));
        Set<String> tags2 = new HashSet<>(List.of(photo2.getTags()));

        tags1.removeAll(tags2); // Removes all elements found in tags2 from tags1
        return tags1.size();

        // int missing = 0;

        // String tags1[] = photo1.getTags();
        // String tags2[] = photo2.getTags();
        // String[] missingTag = new String[max(tags1.length, tags2.length)];
        // for(String tag1: tags1){
        //     boolean found = false;
        //     for(String tag2: tags2){
        //         if(tag1.equals(tag2)){
        //             found = true;
        //             break;
        //         }
        //     }
        //     if(!found){
        //         missingTag[missing] = tag1;
        //         missing++;
        //     }
        // }

        // return missing;
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

    public boolean isContained(Photo photo1, Photo photo2){
        Set<String> names1 = new HashSet<>(List.of(photo1.getName().split(" ")));
        Set<String> names2 = new HashSet<>(List.of(photo2.getName().split(" ")));
        
        names1.retainAll(names2); // Checks for intersection
        return !names1.isEmpty();
        // Boolean isContained = false;
        // String[] name1;
        // String[] name2;
        // if(photo1.getType().equals("C")){name1 = photo1.getName().split(" ");}
        // else{
        //     name1 = new String[1];
        //     name1[0] = photo1.getName();
        // }

        // if(photo2.getType().equals("C")){name2 = photo2.getName().split(" ");}
        // else{
        //     name2 = new String[1];
        //     name2[0] = photo2.getName();
        // }

        // for(String name : name1){
        //     for(String name_ : name2){
        //         if(name.equals(name_)){
        //             isContained = true;
        //             break;
        //         }
        //     }
        // }

        // System.out.println("Name1: " + photo1.getName());
        // System.out.println("Name2: " + photo2.getName());
        // System.out.println("Contained: " + isContained);
        
        // return isContained;
    }
    public static void main(String[] args) {
        hashcode m = new hashcode("c_memorable_moments.txt");
        //m.combinedPhoto();
        // m.printAllInfo();

        // for(int i = 0; i < m.data.size(); i++){
        //     for(int j = i+1; j < m.data.size(); j++){   
        //         if(i != j && !m.isContained(m.data.get(i), m.data.get(j))){
        //             System.out.println("Score: " + m.scoring(m.data.get(i), m.data.get(j))+ "\n");
        //         }
        //     }
        // }
        m.data.parallelStream()
        .forEach(photo1 -> m.data.stream()
            .filter(photo2 -> !m.isContained(photo1, photo2))
            .forEach(photo2 -> {
                System.out.println("Score " + photo1.getName() + " / " + photo2.getName() +  ": " + m.scoring(photo1, photo2) + "\n");
            })
        );

        
    }

}