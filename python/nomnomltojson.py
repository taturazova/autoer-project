import re


def convert(text):
    er_dict = {
        "entities": [],
        "relationships": []
    }

    def parse_relationship(r_line):
        entities = re.findall('\[(.*?)\]', r_line)
        rel = re.search('\](.*?)\[', r_line)
        cardinalities = [x.strip() for x in rel.group(1).split('-')]
        entities_sorted = entities.copy()
        entities_sorted.sort()
        relationship = {
            "entities": entities_sorted,
            entities[0]: cardinalities[0],
            entities[1]: cardinalities[1]
        }
        er_dict["relationships"].append(relationship)

    def parse_entity(e_line):
        attributes = []
        primary_key = []
        partial_primary_keys = []
        e_line = re.search('\[(.*?)\]', e_line)
        split_line = e_line.group(1).split('|')
        entity_name = split_line[0]
        if len(split_line) > 1:
            attributes = [x.strip() for x in split_line[1].split(';')]
            for i, att in enumerate(attributes):
                if '{PK}' in att:
                    attributes[i] = att.strip(' {PK}')
                    primary_key.append(attributes[i])
                if '{PPK}' in att:
                    attributes[i] = att.strip(' {PPK}')
                    partial_primary_keys.append(attributes[i])
        # sorting of the lists here to avoid doing it during marking but could move
            attributes.sort()
            primary_key.sort()
            partial_primary_keys.sort()
        entity = {
            "entity_name": entity_name,
            "primary_key": primary_key,
            "partial_primary_key": partial_primary_keys,
            "attributes": attributes
        }
        er_dict["entities"].append(entity)

    def parse_line(t_line):
        index = t_line.find('-')
        if index == -1:
            parse_entity(t_line)
        else:
            parse_relationship(t_line)

    for line in text.splitlines():
        parse_line(line)

    # er_json = json.dumps(er_dict, indent=4)
    # print(er_json)
    def sort_on_entities(e):
        return e["entities"][0]

    er_dict["relationships"].sort(key=sort_on_entities)
    return er_dict
